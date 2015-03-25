require 'rake'

images = FileList.new("images/**/*.jpg").select do |image| image.include? ("-") end . map do |image| image.gsub("nn", "n").gsub("jy", "j") end

the_pathmap = "master-images/sakana/%-1d/%f"

images.map do |image|
	`cp #{image} #{image.pathmap(the_pathmap)}`
end

