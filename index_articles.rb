require 'rake'

def strip_html(html)
  html.gsub(/<.*?>/, "").gsub(/\s/, "")
end

Article = Struct.new(:name, :text)

sites = Rake::FileList.new("templates/sites/*").pathmap("%f")

article_subdirectories = { "plants" => "shokubutsu", "animals" => "ikimono" }

sites.each do |site|
  Dir.chdir(site) do
    subdirectory = article_subdirectories[site]
    full_articles = Rake::FileList.new("web/#{subdirectory}/*.html")

    articles = full_articles.map { |full_article|
      name = full_article.pathmap("%n")
      content = File.read full_article
      classification = strip_html /<ul class="classification">.*?<\/ul>/m.match(content).to_s
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

    File.write("web/#{subdirectory}/article_list.dart", dart_file_contents)
  end
end
