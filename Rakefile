require 'dimensions'

def compress_images_task(name, source, pathmap, convert_function)
	images = Rake::FileList.new(source)
	compressed_images = images.pathmap(pathmap)
	task name.to_s => compressed_images
	images.each do |image|
		compressed_image = image.pathmap(pathmap)
		file compressed_image => image do
			mkdir_p compressed_image.pathmap('%d')
			sh convert_function.call(image, compressed_image)
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

seisokuchi_quality_settings = Hash.new('57')
seisokuchi_quality_settings['takatsu-chuu.jpg'] = '75'

convert_seisokuchi = lambda do |seisokuchi, compressed_seisokuchi| 
	"convert #{seisokuchi} -resize 1400x\\> -quality #{seisokuchi_quality_settings[seisokuchi.pathmap('%f')]} #{compressed_seisokuchi}"
end

desc "Compress images of fish in master-images and move to workspace"
compress_images_task(:compress_fish_images, "zukan_workspace/master-images/sakana/**/*.jpg", "zukan_workspace/web/images/%-2d/%f", convert_fish)
desc "Compress images of seisokuchi in master-images and move to workspace"
compress_images_task(:compress_seisokuchi_images, "zukan_workspace/master-images/seisokuchi/*.jpg", "zukan_workspace/web/images/seisokuchi/%f", convert_seisokuchi)
desc "Compress general images and move to workspace"
compress_images_task(:compress_general_images, "zukan_workspace/master-images/*.jpg", "zukan_workspace/web/images/%f", convert_seisokuchi)

desc "Parse data in fish_data.txt, generating serialized Python and Dart data structures"
task :generate_fish_list do
	Dir.chdir 'zukan_workspace'
	dependencies = ['fish_data.txt', 'generate_fish_list.py']
	unless (uptodate?('fish_list.pkl', dependencies) and uptodate?('web/fish_list.dart', dependencies))
		sh 'python generate_fish_list.py'
	end
	Dir.chdir '..'
end

desc "Generate html documents using the jinja2 templates engine"
task :generate_pages => :generate_fish_list do
	Dir.chdir 'zukan_workspace'
	dependencies = Rake::FileList.new('templates/**/*')
	unless uptodate?('web/ichiran.html', dependencies)
		sh 'python generate_pages.py'
	end
	Dir.chdir '..'
end

desc "Compile Sass to CSS, using Compass"
task :compile_sass do
	Dir.chdir 'zukan_workspace'
	unless (uptodate?('web/stylesheets/main.css', ['sass/main.scss']))
		sh 'compass compile'
	end
	Dir.chdir '..'
end

desc "Compile everything necessary to use the site with pub serve, part of the Dart SDK, from zukan_workspace"
task :build_workspace => [:compress_fish_images, :compress_seisokuchi_images, :compress_general_images, :generate_pages, :compile_sass]

desc "Compile dart code and produce ready-to-deploy site"
task :compile => :build_workspace do
	Dir.chdir 'zukan_workspace'
	dependencies = Rake::FileList.new('web/**/*')
	unless (uptodate?('build/web/ichiran.html', dependencies))
		sh 'pub build'
		Dir.chdir '..'
		rm_r 'site/static/', :force => true
		cp_r 'zukan_workspace/build/web', 'site/static/'
		sh 'python generate_appcache.py'
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
