
fish_images = Rake::FileList.new("zukan_workspace/master-images/sakana/**/*.jpg")
fish_image_pathmap = "zukan_workspace/web/images/%-2d/%f"
compressed_fish_images = fish_images.pathmap(fish_image_pathmap)

task :fish_images => compressed_fish_images

fish_images.each do |fish_image|
	compressed_fish_image = fish_image.pathmap(fish_image_pathmap)
	file compressed_fish_image => fish_image do
		sh "mkdir -p #{compressed_fish_image.pathmap('%d')}"
		sh "convert #{fish_image} -resize x300 -quality 50 #{compressed_fish_image}"
	end
end