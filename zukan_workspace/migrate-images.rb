require 'rake'

images = FileList.new("images/**/*.jpg").select do |image| image.include? ("-") end 

the_pathmap = "master-images/sakana/%-1d/%f"

images.map do |image|
	`cp #{image} #{image.pathmap(the_pathmap).gsub("nn", "n").gsub("jy", "j").gsub("si", "shi")}`
end

