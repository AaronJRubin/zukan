require 'rake'

class String
  def remove_enclosed(left, right)
    self.gsub(/#{left}.*?#{right}/, "")
  end
end

def strip_html(html)
  html.gsub(/<.*?>/, "").gsub(/\s/, "")
end

Article = Struct.new(:name, :text)

full_articles = Rake::FileList.new("web/ikimono/*.html")

articles = full_articles.map { |full_article|
  name = full_article.pathmap("%n")
  content = File.read full_article
  classification = strip_html /<div class="classification">.*?<\/div>/m.match(content).to_s
  body = strip_html /<article>.*?<\/article>/m.match(content).to_s
  text = "#{classification}。#{body}"
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
