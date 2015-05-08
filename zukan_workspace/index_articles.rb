require 'rake'

class String
  def remove_enclosed(left, right)
    self.gsub(/#{left}.*?#{right}/, "")
  end
end

def process_article(article)
  article.remove_enclosed("{", "}").remove_enclosed("<",">").gsub(/\s/, "")
end

Article = Struct.new(:name, :text)

templates = Rake::FileList.new("templates/base/sakana/*.html")

articles = templates.map { |template|
  name = template.pathmap("%n")
  text = process_article File.read(template)
  Article.new(name, text)
}

dart_articles = articles.map { |article|
  "new Article(\"#{article.name}\", \"#{article.text}\")"
}

article_list_literal = "[#{dart_articles.join(",")}];"

article_list_initializer = "List<Article> article_list = #{article_list_literal}"

article_map_initializer = "Map<String, Article> article_map = new Map.fromIterable(article_list, key: (article) => article.name);"

dart_file_contents = "part of article;\n\n#{article_list_initializer}\n\n#{article_map_initializer}"

File.write("web/article_list.dart", dart_file_contents)




