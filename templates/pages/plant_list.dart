part of plant;

List<Plant> plant_list = [
{% for plant in plants %}
new Plant("{{plant.latin}}", "{{plant.ka}}", "{{plant.zoku}}", "{{plant.romaji}}",
	"{{plant.kana}}", {{plant.rarity}}, {{plant.saitei}}, {{plant.saikou}}, {{plant.iro}}),
{% endfor %}];

Map<String, Plant> plant_map = new Map.fromIterable(plant_list,
    key: (plant) => plant.romaji);
