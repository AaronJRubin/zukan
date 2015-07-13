part of plant;

List<Plant> plant_list = [
{% for plant in plants %}
new Plant(latin: {{plant.latin | dartify}}, romaji: {{plant.romaji | dartify }},
	kana: {{plant.kana | dartify}}, type: {{plant.type | dartify}}, seiikubasho: {{plant.seiikubasho | dartify}}, bunpu: {{plant.bunpu | dartify}},
    kaki: {{plant.kaki}}, kishibeType: {{plant.kishibe_type | dartify}}, iro: {{plant.iro | dartify}}, shokudoku: {{ plant.shokudoku | dartify}}, hanabiraKazu: {{plant.hanabira_kazu | dartify}}),
{% endfor %}];

Map<String, Plant> plant_map = new Map.fromIterable(plant_list,
    key: (plant) => plant.romaji);
