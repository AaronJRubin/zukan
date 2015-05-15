require 'dimensions'
require 'cssminify'
require 'htmlcompressor'

task :default => :compile

workspace = 'zukan_workspace'
master_images = "#{workspace}/master-images"
images = "#{workspace}/web/images"
STATIC_SITE = "site/static"

def maybe_chmod(mode, files)
	if files.class == String
		files = [files]
	end
	files.select { |file| File.exist? file } . each do |file|
		chmod mode, file, verbose: false
	end
end

def lock(files)
	maybe_chmod "a=rx", files
end

def unlock(files)
	maybe_chmod "a=rwx", files
end

def smart_compile_dart(dir)
  Dir.chdir(dir) do
    dart_glob = "web/**/*.dart"
    dart_files = Rake::FileList.new(dart_glob)
    representative_file = Rake::FileList.new("build/web/**/*.dart.js").first
    if representative_file.nil? or not uptodate?(representative_file, dart_files) # a dart file has been modified
      unlock Rake::FileList.new('build/**/*')
      sh 'pub build'
      lock Rake::FileList.new('build/**/*').exclude { |path| File.directory?(path) }
    else
      non_dart_files = Rake::FileList.new("web/**/*").exclude(dart_glob).exclude { |path| File.directory?(path) }
      puts non_dart_files
      non_dart_files.each do |file|
        new_path = file.pathmap("build/%p")
        mkdir_p new_path.pathmap("%d")
        unlock new_path
        cp file, new_path
        lock new_path
      end
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
      unlock compressed_image
      sh convert_function.call(image, compressed_image)
      lock compressed_image
    end
  end
end

NON_ICHIRAN_DIMENSIONS = "278x"
ICHIRAN_HEIGHT = 112
HEADER_WIDTH = 335
LONG_HEADER_IMAGE_MAX_WIDTH = 388

convert_animal = lambda do |animal, compressed_animal|
  if animal.include? "ichiran"	
    dimensions = Dimensions.dimensions(animal)
    width = dimensions[0]	
    height = dimensions[1]	
    aspect_ratio = height.fdiv(width)	
    header_display_height = HEADER_WIDTH * aspect_ratio	
    is_long = height * 2 < width # this determines whether the animal will be at 100% width on screens with size 415 px or less
    if is_long
      header_display_height = LONG_HEADER_IMAGE_MAX_WIDTH * aspect_ratio
    end
    needed_height = [ICHIRAN_HEIGHT, header_display_height].max	
    resize = "x#{needed_height}"
  else
    resize = NON_ICHIRAN_DIMENSIONS
  end
  "convert #{animal} -resize #{resize} -quality 50 #{compressed_animal}"
end

desc "Compress images of animals in master-images and move to workspace"
compress_images_task(:compress_animal_images, "#{master_images}/ikimono/**/*.jpg", "#{images}/%-2d/%f", convert_animal)

quality_override = Hash.new('57')
quality_override['takatsu-chuu.jpg'] = '75'

size_override = Hash.new("1400x\\>")
size_override['takatsugawa-home.jpg'] = '958x'

convert_general = lambda do |image, compressed_image| 
  "convert #{image} -resize #{size_override[image.pathmap('%f')]} -quality #{quality_override[image.pathmap('%f')]} #{compressed_image}"
end

mamechishiki_size_override = Hash.new("459x")
mamechishiki_size_override["ochi-ayu.jpg"] = '459x278!'

convert_mamechishiki = lambda do |image, compressed_image|
  "convert #{image} -resize #{mamechishiki_size_override[image.pathmap('%f')]} -quality 50 #{compressed_image}"
end

desc "Compress images of seisokuchi in master-images and move to workspace"
compress_images_task(:compress_seisokuchi_images, "#{master_images}/seisokuchi/*.jpg", "#{images}/seisokuchi/%f", convert_general)

desc "Compress images for mamechishiki articles and move to workspace"
compress_images_task(:compress_mamechishiki_images, "#{master_images}/mamechishiki/**/*.jpg", "#{images}/mamechishiki/%-1d/%f", convert_mamechishiki)

desc "Compress miscellaneous images and move to workspace"
compress_images_task(:compress_miscellaneous_images, "#{master_images}/*.jpg", "#{images}/%f", convert_general)

desc "Compress all images and move to workspace"
task :compress_images => [:compress_animal_images, :compress_seisokuchi_images, :compress_mamechishiki_images, :compress_miscellaneous_images]

desc "Parse data in animal_data.txt, generating serialized Python and Dart data structures"
task :generate_animal_list do
  Dir.chdir workspace do
    dependencies = ['animal.py', 'animal_data.txt', 'generate_animal_list.py']
    unless (uptodate?('animal_list.pkl', dependencies) and uptodate?('web/animal_list.dart', dependencies))
      unlock 'animal_list.pkl'
      unlock 'web/animal_list.dart'
      sh 'python generate_animal_list.py'
      lock 'animal_list.pkl'
      lock 'web/animal_list.dart'
    end
  end
end

desc "Generate html documents using the jinja2 templates engine"
task :generate_pages => :generate_animal_list do
  Dir.chdir workspace do
    dependencies = Rake::FileList.new('templates/**/*').include('animal.py').include('animal_data.txt').include('generate_animal_list.py')
    unless uptodate?('web/ikimono/ichiran.html', dependencies)
      unlock Rake::FileList.new('web/**/*.html')
      sh 'python generate_pages.py'
    end
    lock Rake::FileList.new('web/**/*.html')
  end
end

desc "Generate dart file that contains text of all articles for client-side searching"
file "#{workspace}/web/article_list.dart" => :generate_pages do |task|
  dependencies = Rake::FileList.new("#{workspace}/web/ikimono/*.html")
  unless uptodate?(task.name, dependencies)
    unlock task.name
    Dir.chdir workspace do
      sh 'ruby index_articles.rb'
    end
    lock task.name
  end
end

desc "Compile Sass to CSS, using Compass"
task :compile_sass do
  Dir.chdir workspace do
    css_file = 'web/stylesheets/main.css'
    unless (uptodate?(css_file, ['sass/main.scss']))
      sh 'compass compile'
    end	
  end
end

desc "Compile everything necessary to use the site with pub serve, part of the Dart SDK, from zukan_workspace"
task :build_workspace => [:compress_images, :generate_pages, :compile_sass, "#{workspace}/web/article_list.dart"]

def generate_appcache
  appcache_path = "#{STATIC_SITE}/takatsugawa-zukan.appcache"
  unlock appcache_path
  File.open(appcache_path, "w") do |appcache| 
    appcache.puts "CACHE MANIFEST"
    appcache.puts "##{Time.now()}"
    files = Rake::FileList.new("#{STATIC_SITE}/**/*.{jpg,html,css,js}").exclude("#{STATIC_SITE}/packages/browser/interop.js") 
    files.each do |file|
      appcache.puts file.gsub("#{STATIC_SITE}/", "")
    end
  end
  lock appcache_path
end

desc "Compile dart code and produce ready-to-deploy site with appcache and minified css"
task :compile => :build_workspace do
  dependencies = Rake::FileList.new("#{workspace}/**/*")
  unless (uptodate?("#{workspace}/build/web/ichiran.html", dependencies))
    rm_r STATIC_SITE, :force => true 
    smart_compile_dart(workspace)
    cp_r "#{workspace}/build/web", STATIC_SITE
    generate_appcache
    css_path = "#{STATIC_SITE}/stylesheets/main.css"
    unlock css_path
    File.write(css_path, CSSminify.compress(File.read(css_path)))
    lock css_path
    compressor = HtmlCompressor::Compressor.new
    htmlFiles = Rake::FileList.new("#{STATIC_SITE}/**/*.html")
    htmlFiles.each do |file|
      unlock file
      File.write(file, compressor.compress(File.read(file)))
      lock file
    end
    jsFiles = Rake::FileList.new("#{STATIC_SITE}/**/*.js")
    jsFiles.each do |file|
      unlock file
      sh "uglifyjs #{file} -c -m -o #{file}" 
      lock file
    end
  end
end

desc "Deploy site to Google App Engine"
task :deploy => :compile do
  Dir.chdir 'site' do
    sh 'appcfg.py --no_cookies update .'
  end
end

desc "Delete all generated files, except for compressed image files"
task :clean_nonimage do
  generated_textfiles = Rake::FileList.new.include("#{workspace}/web/**/*.html").include("#{workspace}/web/**/*.css").include("#{workspace}/web/*_list.dart")
  rm_f generated_textfiles
  rm_f "#{workspace}/animal_list.pkl"
  rm_rf "#{workspace}/build/"
  rm_rf STATIC_SITE
end

desc "Delete all generated files for a clean build"
task :clean => :clean_nonimage do
  rm_rf images
end
