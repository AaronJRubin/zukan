def compress_images_task(name, source, pathmap, convert_function)
	images = Rake::FileList.new(source)
	compressed_images = images.pathmap(pathmap)
	task name.to_s => compressed_images
	images.each do |image|
		compressed_image = image.pathmap(pathmap)
		file compressed_image => image do
			sh "mkdir -p #{compressed_image.pathmap('%d')}"
			sh convert_function.call(image, compressed_image)
		end
	end
end

convert_fish = lambda do |fish, compressed_fish| 
	"convert #{fish} -resize x300 -quality 50 #{compressed_fish}"
end

seisokuchi_quality_settings = Hash.new('57')
seisokuchi_quality_settings['takatsu-chuu.jpg'] = '75'

convert_seisokuchi = lambda do |seisokuchi, converted_seisokuch| 
	"convert #{seisokuchi} -resize 960x -quality #{seisokuchi_quality_settings[seisokuchi.pathmap('%f')]} #{compressed_seisokuchi}"
end

compress_images_task(:compress_fish_images, "zukan_workspace/master-images/sakana/**/*.jpg", "zukan_workspace/web/images/%-2d/%f", convert_fish)
compress_images_task(:compress_seisokuchi_images, "zukan_workspace/master-images/seisokuchi/*.jpg", "zukan_workspace/web/images/seisokuchi/%f", convert_seisokuchi)

task :generate_fish_list do
	Dir.chdir 'zukan_workspace'
	dependencies = ['fish_data.txt', 'generate_fish_list.py']
	unless (uptodate?('fish_list.pkl', dependencies) and uptodate?('web/fish_list.dart', dependencies))
		sh 'python generate_fish_list.py'
	end
	Dir.chdir '..'
end

task :generate_pages => :generate_fish_list do
	Dir.chdir 'zukan_workspace'
	sh 'python generate_pages.py'
	Dir.chdir '..'
end

task :generate_sass do
	Dir.chdir 'zukan_workspace'
	unless (uptodate?('web/stylesheets/main.css', ['sass/main.scss']))
		sh 'compass compile'
	end
	Dir.chdir '..'
end

task :build_workspace => [:compress_fish_images, :compress_seisokuchi_images, :generate_pages, :generate_sass]

task :compile => :build_workspace do
	Dir.chdir 'zukan_workspace'
	sh 'pub build'
	Dir.chdir '..'
	sh 'rm -r site/static/'
	sh 'cp -r zukan_workspace/build/web site/static/'
	sh 'python generate_appcache.py'
end

task :deploy => :compile do
	Dir.chdir 'site'
	sh 'appcfg.py --no_cookies update .'
	Dir.chidr '..'
end