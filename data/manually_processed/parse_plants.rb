require 'csv'
require 'rake'
require 'yaml'

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
  result = data.select { |row| not row[8].nil? } . map { |row|
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
    res["type"] = type
    res
  }  
  return result
end

result = Rake::FileList.new("*.csv").map { |file| parse_plant_file(file) } . flatten

result_map = {}

result.each do |plant|
  result_map[plant["kana"]] = plant
  plant.delete("kana")
end

output_file = File.open("plant_data.yaml", "w")

output_file.write(YAML.dump(result_map))
