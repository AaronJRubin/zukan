require 'dimensions'
require 'cssminify'
require 'htmlcompressor'

task :default => :compile

sites = Rake::FileList.new("templates/sites/*").pathmap("%f")
appengine_sites = Rake::FileList.new("*_appengine/static")
MASTER_IMAGES = "master-images"
article_subdirectories = { "plants" => "shokubutsu", "animals" => "ikimono" }

def compressed_path(image_path)
  split_path = image_path.gsub("#{MASTER_IMAGES}/", "").split("/")
  return "#{split_path[0]}/web/images/#{split_path[1..-1].join("/")}"
end

def glob_disjunct(strings)
  "{#{strings.join(",")}"
end

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

def strip_html(html)
  html.gsub(/<.*?>/, "").gsub(/\s/, "")
end

Article = Struct.new(:name, :text)

sites.each do |site|
  task "index_articles_#{site}" do
    Dir.chdir(site) do
      subdirectory = article_subdirectories[site]
      full_articles = Rake::FileList.new("web/#{subdirectory}/*.html")
      destination = "web/#{subdirectory}/article_list.dart"

      unless uptodate?(destination, full_articles)
        unlocked(destination) do
          articles = full_articles.map { |full_article|
            name = full_article.pathmap("%n")
            content = File.read full_article
            classification = strip_html /<ul class="classification">.*?<\/ul>/m.match(content).to_s
            body = strip_html /<article>.*?<\/article>/m.match(content).to_s
            text = "#{classification}。#{body}"
            Article.new(name, text)
          }

          dart_articles = articles.map { |article|
            "new Article(\"#{article.name}\", \"#{article.text}\")"
          }

          article_list_literal = "[#{dart_articles.join(",")}];"

          article_list_initializer = "List<Article> article_list = #{article_list_literal}"

          article_map_initializer = "Map<String, Article> article_map = new Map.fromIterable(article_list, key: (article) => article.name);"

          dart_file_contents = "part of article;\n\n#{article_list_initializer}\n\n#{article_map_initializer}"

          File.write(destination, dart_file_contents)

          puts "Articles indexed for #{site}"
        end
      end
    end
  end
end

desc "Index articles (producing a dart file named article_list.dart for every site, containing article text)"
task :index_articles => sites.map { |site| "index_articles_#{site}" }

# This function generates a task for compressing all of the images in a directory,
# given a name for the task, the source directory,
# and a lambda that, when given two strings, one for the path to the original image
# and one for the path to the compressed image, generates the shell command - a string - needed
# to produce the compressed image from the original image. That shell command will probably
# use the 'convert' utility in ImageMagick.
def compress_images_task(name, source, convert_function)
  images = Rake::FileList.new("#{MASTER_IMAGES}/#{source}")
  compressed_images = images.map { |image| compressed_path(image) }
  multitask name.to_s => compressed_images
  images.each do |image|
    compressed_image = compressed_path(image)
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


NON_ICHIRAN_DIMENSIONS = "278x"
# This is the highest an ichiran image gets, until short images and long images diverge
ICHIRAN_IMAGE_HEIGHT = 133
# Short images become very tall right at the breakpoint where they become half the screen
# Because short images have an aspect ratio of 4x3 (where 4 is width and 3 is height),
# we don't actually have to use this value to optimize image size, but it's good to have
# it here so that we don't forget that.
SHORT_IMAGE_ICHIRAN_MAX_HEIGHT = 144
HEADER_IMAGE_WIDTH = 335
# long images become very long right at the breakpoint where image and classification information go onto separate rows
# and also at the breakpoint where they need to start filling up the entire width of the ichiran screen (both are 450px at the moment)
LONG_IMAGE_HEADER_MAX_WIDTH = 433

convert_animal = lambda do |animal, compressed_animal|
  if animal.include? "ichiran"	
    aspect_ratio = get_cropped_aspect_ratio(animal) # remember, height / width here!
    header_display_height = HEADER_IMAGE_WIDTH * aspect_ratio	
    is_long = aspect_ratio < 0.5 
    if is_long
      header_display_height = LONG_IMAGE_HEADER_MAX_WIDTH * aspect_ratio
    end
    needed_height = [ICHIRAN_IMAGE_HEIGHT, header_display_height].max	
    resize = "x#{needed_height}"
  else
    resize = NON_ICHIRAN_DIMENSIONS
  end
  return convert(animal, compressed_animal, resize = resize, quality = "60")
end

desc "Compress images of animals in master-images and move to workspace"
compress_images_task(:compress_animal_images, "animals/ikimono/**/*.jpg", convert_animal)

convert_plant = lambda do |plant, compressed_plant|
  return convert(plant, compressed_plant, resize = "#{HEADER_IMAGE_WIDTH}x", quality = "60")
end

desc "Compress images of plants in master-images and move to workspace"
compress_images_task(:compress_plant_images, "plants/shokubutsu/**/*.jpg", convert_plant)

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
compress_images_task(:compress_seisokuchi_images, "animals/seisokuchi/*.jpg", convert_general)

desc "Compress images for mamechishiki articles and move to workspace"
compress_images_task(:compress_mamechishiki_images, "animals/mamechishiki/**/*.jpg", convert_mamechishiki)

desc "Compress miscellaneous images and move to workspace"
compress_images_task(:compress_miscellaneous_images, "**/*.jpg", convert_general)

desc "Compress all images and move to workspace"
task :compress_images => [:compress_animal_images, :compress_plant_images, :compress_seisokuchi_images, :compress_mamechishiki_images, :compress_miscellaneous_images]

desc "Validate yaml data for which a schema is defined"
task :validate_data do 
  data_files = Rake::FileList.new('data/**/*.yaml')
  data_files.each do |data_file|
    schema_file = data_file.pathmap("%X.schema")
    if File.exists? schema_file
      sh "kwalify -f #{schema_file} #{data_file}"
    end
  end
end


desc "Render templates (html and others) using the jinja2 template engine"
task :generate_pages => [:compress_images, :validate_data] do
  dependencies = Rake::FileList.new('templates/**/*').include("#{MASTER_IMAGES}/**/*").include('animal.py').include('plant.py').include('data/**/*')
  unless uptodate?('animals/web/ikimono/ichiran.html', dependencies)
    sh 'python generate_pages.py' 
  end
end

=begin
desc "Generate dart file that contains text of all articles for client-side searching"
task :index_articles => :generate_pages do
  dependencies = Rake::FileList.new("animals/web/ikimono/*.html").include("plants/web/shokubutsu/*.html")
  unless uptodate?("animals/web/ikimono/article_list.dart", dependencies)
    unlocked ["animals/web/ikimono/article_list.dart", "plants/web/shokubutsu/article_list.dart"] do
      sh 'ruby index_articles.rb'
    end
  end
end
=end

sites.each do |site|
  task "#{site}_compass_watch" do
    system "compass watch --sass-dir sass --css-dir #{site}/web/stylesheets"
  end
end

multitask compass_watch: sites.map { |site| "#{site}_compass_watch" }

desc "Compile Sass to CSS, using Compass"
task :compile_sass do
  css_file = 'animals/web/stylesheets/main.css'
  unless (uptodate?(css_file, ['sass/main.scss']))
    sites.each do |site|
      sh "compass compile --sass-dir sass --css-dir #{site}/web/stylesheets"
    end
  end	
end

desc "Compile everything necessary to use the site with pub serve, part of the Dart SDK (output in web)"
task :build_web => [:compress_images, :generate_pages, :compile_sass, :index_articles]

sites.each do |site|
  desc "Run development pub server for #{site} site (Dart SDK required)"
  task "serve_#{site}" => :build_web do
    Dir.chdir(site) do
      sh 'pub serve --port 0'
    end
  end
end

def generate_appcache(dir)
  appcache_path = "#{dir}/takatsugawa-zukan.appcache"
  unlocked appcache_path do
    File.open(appcache_path, "w") do |appcache| 
      appcache.puts "CACHE MANIFEST"
      appcache.puts "##{Time.now()}"
      files = Rake::FileList.new("#{dir}/**/*.{jpg,html,css,js}").exclude("#{dir}/packages/browser/interop.js") 
      files.each do |file|
        appcache.puts file.gsub("#{dir}/", "")
      end
    end
  end
end

desc "Compile dart code and produce ready-to-deploy site with appcache and minified css"
task :compile => :build_web do
  # Yes, the dependency for this task is everything.
  dependencies = Rake::FileList.new("**/*").exclude(glob_disjunct appengine_sites).exclude("#{glob_disjunct appengine_sites}/**/*")
  sites.each do |site|
    appengine_site = "#{site}_appengine/static"
    unless (uptodate?("#{appengine_site}/home.html", dependencies)) 
      rm_r appengine_site, :force => true
      smart_compile_dart(site)
      cp_r "#{site}/build/web", appengine_site
      generate_appcache appengine_site
      css_path = "#{appengine_site}/stylesheets/main.css"
      unlocked css_path do
        File.write(css_path, CSSminify.compress(File.read(css_path)))
      end
      compressor = HtmlCompressor::Compressor.new
      htmlFiles = Rake::FileList.new("#{appengine_site}/**/*.html")
      htmlFiles.each do |file|
        unlocked file do
          File.write(file, compressor.compress(File.read(file)))
        end
      end
      jsFiles = Rake::FileList.new("#{appengine_site}/**/*.js")
      jsFiles.each do |file|
        unlock file
        sh "uglifyjs #{file} -c -m -o #{file}" 
        lock file
      end
    end
  end
end

sites.each do |site|
  desc "Deploy #{site} site to Google App Engine"
  task "deploy_#{site}" => :compile do
    Dir.chdir site do
      sh 'appcfg.py --no_cookies update .'
    end
  end
end

desc "Delete all generated files, except for compressed image files"
task :clean_nonimage do
  sites.each do |site|
    Dir.chdir(site) do 
      generated_textfiles = Rake::FileList.new.include("**/*{html,css,_list.dart}")
      rm_f generated_textfiles
      rm_rf "build"
    end
    rm_rf appengine_sites
  end
end

desc "Delete all generated files for a clean build"
task :clean => :clean_nonimage do
  sites.each do |site|
    Dir.chdir(site) do
      rm_rf 'web/images'
    end
  end
end
