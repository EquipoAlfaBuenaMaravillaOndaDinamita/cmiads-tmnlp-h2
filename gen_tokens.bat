scrapy crawl pagination -a tokens=150 -a topic=art -O data/tokens_art.csv
scrapy crawl pagination -a tokens=150 -a topic=basketball -O data/tokens_basketball.csv
scrapy crawl pagination -a tokens=150 -a topic=f1 -O data/tokens_f1.csv
scrapy crawl pagination -a tokens=150 -a topic=food -O data/tokens_food.csv
scrapy crawl pagination -a tokens=150 -a topic=geography -O data/tokens_geography.csv
scrapy crawl pagination -a tokens=150 -a topic=golf -O data/tokens_golf.csv
scrapy crawl pagination -a tokens=150 -a topic=history -O data/tokens_history.csv
scrapy crawl pagination -a tokens=150 -a topic=music -O data/tokens_music.csv
scrapy crawl pagination -a tokens=150 -a topic=science -O data/tokens_science.csv
scrapy crawl pagination -a tokens=150 -a topic=sports -O data/tokens_sports.csv
scrapy crawl pagination -a tokens=150 -a topic=technology -O data/tokens_technology.csv
copy data/tokens_art.csv + data/tokens_basketball.csv + data/tokens_f1.csv + data/tokens_food.csv + data/tokens_geography.csv + data/tokens_golf.csv + data/tokens_history.csv + data/tokens_music.csv + data/tokens_science.csv + data/tokens_sports.csv + data/tokens_technology.csv data\tokens_topics.csv