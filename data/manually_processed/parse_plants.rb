require 'csv'
require 'rake'
require 'yaml'
require 'moji'
require 'romkan'

def parse_kaki(kaki_string)
  if kaki_string == nil
    return []
  end
  kaki_string = kaki_string.gsub("通年", "1〜12").gsub("春〜秋", "4〜11").gsub("夏〜秋", "6〜11").
    gsub("晩秋〜冬季紅葉", "").gsub("秋", "9〜11").gsub("（稀）", "").strip  
  if kaki_string.length == 0
    return []
  elsif kaki_string.length == 1
    return [kaki_string.to_i]
  else
    start, stop = kaki_string.split("〜").map(&:to_i)
    return start.upto(stop).to_a
  end
end

TYPE_MAP = { "tanshiyou" => "単子葉植物", "soushiyou" => "双子葉植物", "shida" => "シダ類" }

def parse_plant_file(plant_file)
  data = CSV.read(plant_file)[2..-1] # first two lines are headings
  type = TYPE_MAP[plant_file.gsub(".csv", "")] 
  result = data.select { |row| not row[0].nil? } . map { |row|
    res = {}
    row = row.map { |value| if value.nil? then value else value.strip.gsub("　", "").gsub("~", "〜") end }
    seiikubasho = []
    if row[1] != nil
      seiikubasho << "沈水"
    end
    if row[2] != nil
      seiikubasho << "浮葉"
    end
    if row[3] != nil
      seiikubasho << "浮標"
    end
    if row[4] != nil
      seiikubasho << "抽水"
    end
    if row[5] != nil
      seiikubasho << "湿地・岸辺"
      if row[5].include?("砂浜")
        kishibe_type = "砂浜"
      elsif row[5].include?("kaigan")
        kishibe_type = "海岸"
      elsif row[5].include?("kaiganiwaba")
        kishibe_type = "海岸岩場"
      end
      if not kishibe_type.nil?
        res["kishibe_type"] = kishibe_type
      end
    end
    res["seiikubasho"] = seiikubasho 
    kaki = parse_kaki(row[6])
    res["kaki"] = kaki
    # skip tokki for now
    res["latin"] = row[8]
    res["kana"] = row[9]
		res["bunpu"] = if row[10].nil? then [] else row[10].gsub(/[()（） 　]/, "").chars.select { |char| char != "" } end
		if type != "シダ類"
			#puts "Parsing search parameters for plant of type #{type}"
			res["hanotsukikata"] = row[11]
			#puts "hananotsukikata = #{row[11]}"
			res["hanokatachi"] = row[12]
			#puts "hanokatachi = #{row[12]}"
			res["kyoshi"] = row[13]
			#puts "kyoshi = #{row[13]}"
			res["hananotsukikata"] = row[14]
			#puts "hananotsukikata = #{row[14]}"
			petal_description = row[15] || ""
			res["petal_description"] = petal_description
			#puts "petal_description = #{row[15]}"
			petal_counts = Set.new(petal_description.scan(/\d+/).map(&:to_i))
			petal_ranges = petal_description.scan(/\d+〜\d+/)
			petal_ranges.each do |petal_range|
				puts "Parsing petal range: #{petal_range}"
				beginning, ending = petal_range.split("〜").map(&:to_i)
				((beginning + 1)...ending).each do |quantity|
					petal_counts.add(quantity)
				end
			end
			res["petal_counts"] = petal_counts.to_a.sort
			#puts "petal_counts = #{res["petal_counts"]}"
			res["color_description"] = row[16]
			#puts "color_description = #{row[16]}"
			#res["colors"] = row[16].split(/[・、～/
			#puts "shokudoku = #{row[17]
			shokudoku_description = row[17] || "不明"
			res["shokudoku"] = shokudoku_description.gsub("・近縁種は毒", "").gsub("・沖縄「ンジャナ」", "").split("・")
		end
		res["type"] = type
		res
	}  
	return result
end

result = Rake::FileList.new("*.csv").map { |file| parse_plant_file(file) } . flatten

result_map = {}

result.each do |plant|
	katakana = plant["kana"]
	hiragana = Moji.kata_to_hira(katakana)
	romaji = hiragana.to_roma.gsub("n'", "nn")
	plant.delete("kana")
	result_map[romaji] = plant
end

output_file = File.open("plant_data.yaml", "w")

output_file.write(YAML.dump(result_map))
