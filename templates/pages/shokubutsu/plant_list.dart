part of plant;

List<Plant> plant_list = [
{% for plant in plants %}
new Plant(latin: "{{plant.latin}}", romaji: "{{plant.romaji}}",
	kana: "{{plant.kana}}", type: "{{plant.type}}", seiikubasho: {{plant.dart_seiikubasho()}}, bunpu: {{plant.dart_bunpu()}},
    kaki: {{plant.kaki}}, ganpenType: "{{plant.ganpen_type}}"),
{% endfor %}];

Map<String, Plant> plant_map = new Map.fromIterable(plant_list,
    key: (plant) => plant.romaji);
