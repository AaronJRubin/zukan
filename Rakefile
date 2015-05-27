require 'dimensions'
require 'cssminify'
require 'htmlcompressor'

task :default => :compile

MASTER_IMAGES = "master-images"
IMAGES = "web/images"
STATIC_SITE = "appengine_build/static"

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

def unlocked(files)
  unlock files
  yield
  lock files
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
      non_dart_files.each do |file|
        new_path = file.pathmap("build/%p")
        mkdir_p new_path.pathmap("%d")
        unlocked new_path do
          cp file, new_path
        end
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
    dependencies = [image]
    crop_settings = image.pathmap("%X.crp")
    if File.exists? crop_settings
      dependencies << crop_settings
    end
    file compressed_image => dependencies do
      mkdir_p compressed_image.pathmap('%d')
      unlocked compressed_image do
        sh convert_function.call(image, compressed_image)
      end
    end
  end
end

NON_ICHIRAN_DIMENSIONS = "278x"
ICHIRAN_HEIGHT = 133
HEADER_WIDTH = 335
LONG_HEADER_IMAGE_MAX_WIDTH = 388

# Aspect ratio is height / width here
def get_cropped_aspect_ratio(image)
  uncropped_dimensions = Dimensions.dimensions(image)
  uncropped_width = uncropped_dimensions[0].to_f
  uncropped_height = uncropped_dimensions[1].to_f
  crop_file = image.pathmap("%X.crp")
  if not File.exists? crop_file
   return uncropped_height / uncropped_width
  else
    crop_string = File.read(crop_file).strip
    cropped_dimensions = /(\d+)x(\d+)/.match(crop_string)
    cropped_width = cropped_dimensions[1].to_f
    cropped_height = cropped_dimensions[2].to_f
    return cropped_height / cropped_width
  end
end
  

def convert(source, target, resize = "300x300", quality = "50")
  crop_file = source.pathmap("%X.crp")
  if File.exists? crop_file
    crop_string = File.read(crop_file).strip
    crop_command = "-crop #{crop_string}"
  else
    crop_command = ""
  end
  return "convert #{source} #{crop_command} -resize #{resize} -quality #{quality} #{target}"
end

convert_animal = lambda do |animal, compressed_animal|
  if animal.include? "ichiran"	
    aspect_ratio = get_cropped_aspect_ratio(animal)
    header_display_height = HEADER_WIDTH * aspect_ratio	
    is_long = aspect_ratio < 0.5 #this determines whether the animal will be at 100% width on screens with size 415 px or less
    if is_long
      header_display_height = LONG_HEADER_IMAGE_MAX_WIDTH * aspect_ratio
    end
    needed_height = [ICHIRAN_HEIGHT, header_display_height].max	
    resize = "x#{needed_height}"
  else
    resize = NON_ICHIRAN_DIMENSIONS
  end
  return convert(animal, compressed_animal, resize = resize, quality = "60")
end

desc "Compress images of animals in master-images and move to workspace"
compress_images_task(:compress_animal_images, "#{MASTER_IMAGES}/ikimono/**/*.jpg", "#{IMAGES}/%-2d/%f", convert_animal)

quality_override = Hash.new('57')
quality_override['takatsu-chuu.jpg'] = '75'

size_override = Hash.new("1400x\\>")
size_override['takatsugawa-home.jpg'] = '958x'

convert_general = lambda do |image, compressed_image| 
  name = image.pathmap('%f')
  return convert(image, compressed_image, resize = size_override[name], quality = quality_override[name]) 
end

mamechishiki_size_override = Hash.new("459x")
mamechishiki_size_override["ochi-ayu.jpg"] = '459x278!'

convert_mamechishiki = lambda do |image, compressed_image|
  return convert(image, compressed_image, resize = mamechishiki_size_override[image.pathmap('%f')], quality = "50")
end

desc "Compress images of seisokuchi in master-images and move to workspace"
compress_images_task(:compress_seisokuchi_images, "#{MASTER_IMAGES}/seisokuchi/*.jpg", "#{IMAGES}/seisokuchi/%f", convert_general)

desc "Compress images for mamechishiki articles and move to workspace"
compress_images_task(:compress_mamechishiki_images, "#{MASTER_IMAGES}/mamechishiki/**/*.jpg", "#{IMAGES}/mamechishiki/%-1d/%f", convert_mamechishiki)

desc "Compress miscellaneous images and move to workspace"
compress_images_task(:compress_miscellaneous_images, "#{MASTER_IMAGES}/*.jpg", "#{IMAGES}/%f", convert_general)

desc "Compress all images and move to workspace"
task :compress_images => [:compress_animal_images, :compress_seisokuchi_images, :compress_mamechishiki_images, :compress_miscellaneous_images]

desc "Validate yaml data for which a schema is defined"
task :validate_data do 
  data_files = Rake::FileList.new('data/**/*.yaml')
  data_files.each do |data_file|
    schema_file = data_file.pathmap("%X.schema")
    if File.exists? schema_file
      sh "kwalify -lf #{schema_file} #{data_file}"
    end
  end
end


desc "Generate html (and one Dart file) documents using the jinja2 templates engine"
task :generate_pages => [:compress_images, :validate_data] do
  dependencies = Rake::FileList.new('templates/**/*').include('web/images/ikimono/**/*').include('animal.py').include('data/**/*')
  unless uptodate?('web/ikimono/ichiran.html', dependencies)
    unlock Rake::FileList.new('web/**/*.html').include("web/ikimono/animal_list.dart")
    sh 'python generate_pages.py'
    lock Rake::FileList.new('web/**/*.html').include("web/ikimono/animal_list.dart")
  end
end

desc "Generate dart file that contains text of all articles for client-side searching"
file "web/article_list.dart" => :generate_pages do |task|
  dependencies = Rake::FileList.new("web/ikimono/*.html")
  unless uptodate?(task.name, dependencies)
    unlocked task.name do
      sh 'ruby index_articles.rb'
    end
  end
end

desc "Compile Sass to CSS, using Compass"
task :compile_sass do
  css_file = 'web/stylesheets/main.css'
  unless (uptodate?(css_file, ['sass/main.scss']))
    sh 'compass compile'
  end	
end

desc "Compile everything necessary to use the site with pub serve, part of the Dart SDK (output in web)"
task :build_web => [:compress_images, :generate_pages, :compile_sass, "web/article_list.dart"]

desc "Run development pub server (Dart SDK required)"
task :serve => :build_web do
  sh 'pub serve'
end

def generate_appcache
  appcache_path = "#{STATIC_SITE}/takatsugawa-zukan.appcache"
  unlocked appcache_path do
    File.open(appcache_path, "w") do |appcache| 
      appcache.puts "CACHE MANIFEST"
      appcache.puts "##{Time.now()}"
      files = Rake::FileList.new("#{STATIC_SITE}/**/*.{jpg,html,css,js}").exclude("#{STATIC_SITE}/packages/browser/interop.js") 
      files.each do |file|
        appcache.puts file.gsub("#{STATIC_SITE}/", "")
      end
    end
  end
end

desc "Compile dart code and produce ready-to-deploy site with appcache and minified css"
task :compile => :build_web do
  # Yes, the dependency for this task is everything.
  dependencies = Rake::FileList.new("**/*").exclude(STATIC_SITE).exclude("#{STATIC_SITE}/**/*")
  unless (uptodate?("#{STATIC_SITE}/home.html", dependencies))
    rm_r STATIC_SITE, :force => true 
    smart_compile_dart(".")
    cp_r "build/web", STATIC_SITE
    generate_appcache
    css_path = "#{STATIC_SITE}/stylesheets/main.css"
    unlocked css_path do
      File.write(css_path, CSSminify.compress(File.read(css_path)))
    end
    compressor = HtmlCompressor::Compressor.new
    htmlFiles = Rake::FileList.new("#{STATIC_SITE}/**/*.html")
    htmlFiles.each do |file|
      unlocked file do
        File.write(file, compressor.compress(File.read(file)))
      end
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
  Dir.chdir STATIC_SITE do
    sh 'appcfg.py --no_cookies update .'
  end
end

desc "Delete all generated files, except for compressed image files"
task :clean_nonimage do
  generated_textfiles = Rake::FileList.new.include("web/**/*.html").include("web/**/*.css").include("web/*_list.dart")
  rm_f generated_textfiles
  rm_rf "build"
  rm_rf STATIC_SITE
end

desc "Delete all generated files for a clean build"
task :clean => :clean_nonimage do
  rm_rf IMAGES
end
