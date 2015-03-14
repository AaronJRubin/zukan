def full_path(fish_image)
	"zukan_workspace/master-images/sakana/#{fish_image}"
end

Dir.chdir "zukan_workspace/master-images/sakana"
fish_images = Rake::FileList.new("**/*.jpg")
compressed_fish_images = fish_images.pathmap("zukan_workspace/web/images/sakana/%p")
Dir.chdir "../../.."

task :fish_images => compressed_fish_images

fish_images.each do |fish_image|
	compressed_fish_image = "zukan_workspace/web/images/sakana/#{fish_image}"
	file compressed_fish_image => full_path(fish_image) do
		sh "mkdir -p zukan_workspace/web/images/sakana/#{File.dirname(fish_image)}"
		sh "convert #{full_path(fish_image)} -resize x300 -quality 50 #{compressed_fish_image}"
	end
end