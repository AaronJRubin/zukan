part of animal;

List<Animal> animal_list = [
{% for animal in animals %}
new Animal("{{animal.latin}}", "{{animal.ka}}", "{{animal.zoku}}", "{{animal.romaji}}",
	"{{animal.kana}}", {{animal.rarity}}, {{animal.takatsu}}, {{animal.masuda}}),
{% endfor %}];

Map<String, Animal> animal_map = new Map.fromIterable(animal_list,
    key: (animal) => animal.romaji);
