require 'dimensions'
require 'cssminify'
require 'htmlcompressor'

workspace = 'zukan_workspace'

def lock(files)
	chmod "a=rx", files
end

def unlock(files)
	chmod "a=rwx", files
end

def smart_compile_dart
	source_dir = "web"
	build_dir_pathmap = "build/%p"
	dart_files = Rake::FileList.new(source_dir.pathmap("%p/**/*.dart"))
	representative_file = Rake::FileList.new(source_dir.pathmap(build_dir_pathmap).pathmap("%p/**/*.dart.js")).first
	if representative_file.nil? or not uptodate?(representative_file, dart_files) # a dart file has been modified
		unlock Rake::FileList.new('build/**/*')
		sh 'pub build'
		lock Rake::FileList.new('build/**/*')
	else
		non_dart_files = Rake::FileList.new(source_dir.pathmap("%p/**/*")).exclude("*.dart").exclude { |path| File.directory?(path) }
		non_dart_files.each do |file|
			new_path = file.pathmap(build_dir_pathmap)
			mkdir_p new_path.pathmap("%d")
			cp file, new_path
		end
	end
end

# This function generates a task for compressing all of the images in a directory,
# given a name for the task, the source directory, a pathmap for going from an image
# file in the source directory to the corresponding image file in the destination directory,
# and a lambda that, when given two strings, one for the path to the original image
# and one for the path to the compressed image, generates the shell command - a string - needed
# to produce the compressed image from the original image. That shell command will probably
# use the 'convert' utility in ImageMagick.
def compress_images_task(name, source, pathmap, convert_function)
	images = Rake::FileList.new(source)
	compressed_images = images.pathmap(pathmap)
	task name.to_s => compressed_images
	images.each do |image|
		compressed_image = image.pathmap(pathmap)
		file compressed_image => image do
			mkdir_p compressed_image.pathmap('%d')
			sh convert_function.call(image, compressed_image)
			lock compressed_image
		end
	end
end

NON_ICHIRAN_DIMENSIONS = "280x"
ICHIRAN_HEIGHT = 112
HEADER_WIDTH = 335

convert_fish = lambda do |fish, compressed_fish|
 	if fish.include? "ichiran"	
		dimensions = Dimensions.dimensions(fish)
		width = dimensions[0]	
		height = dimensions[1]	
		aspect_ratio = height.fdiv(width)	
		header_display_height = HEADER_WIDTH * aspect_ratio	
		needed_height = [ICHIRAN_HEIGHT, header_display_height].max	
		resize = "x#{needed_height}"
	else
		resize = NON_ICHIRAN_DIMENSIONS
	end
	"convert #{fish} -resize #{resize} -quality 50 #{compressed_fish}"
end

desc "Compress images of fish in master-images and move to workspace"
compress_images_task(:compress_fish_images, "#{workspace}/master-images/sakana/**/*.jpg", "#{workspace}/web/images/%-2d/%f", convert_fish)

quality_override = Hash.new('57')
quality_override['takatsu-chuu.jpg'] = '75'

size_override = Hash.new("1400x\\>")
size_override['takatsugawa-home.jpg'] = '960x'

convert_general = lambda do |image, compressed_image| 
	"convert #{image} -resize #{size_override[image.pathmap('%f')]} -quality #{quality_override[image.pathmap('%f')]} #{compressed_image}"
end

desc "Compress images of seisokuchi in master-images and move to workspace"
compress_images_task(:compress_seisokuchi_images, "#{workspace}/master-images/seisokuchi/*.jpg", "#{workspace}/web/images/seisokuchi/%f", convert_general)
desc "Compress miscellaneous images and move to workspace"
compress_images_task(:compress_miscellaneous_images, "#{workspace}/master-images/*.jpg", "#{workspace}/web/images/%f", convert_general)

desc "Compress all images and move to workspace"
task :compress_images => [:compress_fish_images, :compress_seisokuchi_images, :compress_miscellaneous_images]

desc "Parse data in fish_data.txt, generating serialized Python and Dart data structures"
task :generate_fish_list do
	Dir.chdir workspace
	dependencies = ['fish.py', 'fish_data.txt', 'generate_fish_list.py']
	unless (uptodate?('fish_list.pkl', dependencies) and uptodate?('web/fish_list.dart', dependencies))
		sh 'python generate_fish_list.py'
	end
	lock 'fish_list.pkl'
	lock 'web/fish_list.dart'
	Dir.chdir '..'
end

desc "Generate html documents using the jinja2 templates engine"
task :generate_pages => :generate_fish_list do
	Dir.chdir workspace
	dependencies = Rake::FileList.new('templates/**/*').include('fish.py').include('fish_data.txt').include('generate_fish_list.py')
	unless uptodate?('web/ichiran.html', dependencies)
		sh 'python generate_pages.py'
	end
	lock Rake::FileList.new('web/**/*.html')
	Dir.chdir '..'
end

desc "Compile Sass to CSS, using Compass"
task :compile_sass do
	Dir.chdir workspace
	unless (uptodate?('web/stylesheets/main.css', ['sass/main.scss']))
		sh 'compass compile'
	end
	lock 'web/stylesheets/main.css'
	Dir.chdir '..'
end

desc "Compile everything necessary to use the site with pub serve, part of the Dart SDK, from zukan_workspace"
task :build_workspace => [:compress_images, :generate_pages, :compile_sass]

desc "Compile dart code and produce ready-to-deploy site with appcache and minified css"
task :compile => :build_workspace do
	Dir.chdir workspace
	dependencies = Rake::FileList.new('web/**/*')
	unless (uptodate?('build/web/ichiran.html', dependencies))
		smart_compile_dart	
		Dir.chdir '..'
		rm_r 'site/static/', :force => true
		cp_r "#{workspace}/build/web", 'site/static/'
		sh 'python generate_appcache.py'
		lock 'site/static/takatsugawa-zukan.appcache'
		css_path = 'site/static/stylesheets/main.css'
		unlock css_path
		File.write(css_path, CSSminify.compress(File.read(css_path)))
		lock css_path
		compressor = HtmlCompressor::Compressor.new
		htmlFiles = Rake::FileList.new('site/static/**/*.html')
		htmlFiles.each do |file|
			unlock file
			File.write(file, compressor.compress(File.read(file)))
			lock file
		end
	else
		Dir.chdir '..'
	end
end

desc "Deploy site to Google App Engine"
task :deploy => :compile do
	Dir.chdir 'site'
	sh 'appcfg.py --no_cookies update .'
	Dir.chdir '..'
end

desc "Delete all generated files for a clean build"
task :clean do
	generated_textfiles = Rake::FileList.new.include("#{workspace}/web/**/*.html").include("#{workspace}/web/**/*.css").include("#{workspace}/web/fish_list.dart")
	rm_f generated_textfiles
	rm_f "#{workspace}/fish_list.pkl"
	rm_rf "#{workspace}/web/images/"
	rm_rf "#{workspace}/build/"
	rm_rf "static/static/"
end
