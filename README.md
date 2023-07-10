## Objective
This project involves designing and implementing a big data system that performs real-time streaming analytics for public repositories hosted on GitHub. The system runs a stream processing pipeline, where the live data stream to be analyzed is coming from GitHub API. An Apache Spark cluster processes the data stream. A web application receives the output from Spark and visualizes the analysis result. In this project, I followed the requirements to write codes (Python, Bash, YAML scripts, Dockerfiles) that implement such a streaming process pipeline, which is a multi-container system based on Docker and Docker Compose.

GitHub is one of the most impactful git platforms, which is home to more than 73 million developers and over 200 million repositories, including at least 28 million public repositories as of November 2021. Analysis of software repositories hosted on GitHub has always played a key role in empirical software engineering. The trending analysis based on GitHub repositories and open-source codes, such as top programming languages, prevalent code smells, commit message conventions, and commit frequency distributions, can shed light on the evolution of open-source software and improve DevOps practices. 

![System Architecture](System_Architecture.png)

## Awareness

* You may clone this repository to your local directory.
* Make sure your version Python >= 3.7.0.
* Change to CRLF line terminators for Windows.
* GitHub Search API has a rate limit of 30 requests per minute for authenticated requests. The rate limit allows you to make up to 10 requests per minute for unauthenticated requests. Thus, you need a GitHub personal access token (PAT) to make requests in the data source service. You can follow [these steps](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) to get a PAT.
* Once you obtain PAT, you can replace the URL in `docker-compose.yaml` under data-source environment.
* You need Docker installed on your local machine to run this project. With command as follow
```
docker-compose up
```
* Get the container ID of the spark master and start streaming
```
docker ps
docker exec streaming_spark_1 spark-submit /streaming/spark_app.py
```
## Sparking Streaming Application

1. `data_source.py` service uses Python programing language, which collects information about the most recently-pushed repositories that use any of the three programming languages as the primary coding language through GitHub API. The Python scripts collect and push the new data to Spark at an interval of around 15 seconds, the scripts print the data being sent to Spark using the `print()` function. (The three default languages are JAVA, Python, and C#, You can modify by yourself in `data_source.py` from line 27 to 31 and change the following endpoint to a specific programming language you want.)
```
https://api.github.com/search/repositories?q=+language:{$Programming Language}&sort=updated&order=desc&per_page=50
```

2. `spark_app.py` receives the streaming data, divides it into batches at an interval of 60 seconds (batch duration is 60 seconds), and performs the following four analysis tasks.
   1. Compute the total number of the collected repositories since the start of the streaming application for each of the three programming languages.
   2. Compute the number of the collected repositories with changes pushed during the last 60 seconds.
   3. Compute the average number of stars of all the collected repositories since the start of the streaming application for each of the three programming languages.
   4. Find the top 10 most frequent words in the description of all the collected repositories since the start of the streaming application for each of the three programming languages.
   5. Print the analysis results for each batch.

3. `flash_app.py`, a web service listening on port 5000, which receives the analysis results from Spark and visualizes them in real-time. The web service runs a dashboard web application that includes:
    1. Three numbers that tell the total number of the collected repositories since the start of the streaming application for each of the three programming languages in real-time. The numbers are updated every 60 seconds.
    2. A real-time line chart that shows the number of the recently-pushed repositories during each batch interval (60 seconds) for each of the three programming languages. The chart is updated every 60 seconds.
    3. A real-time bar plot that shows the average number of stars of all the collected repositories since the start of the streaming application for each of the three programming languages. The bar plot is updated every 60 seconds.
    4. Three lists that contain the top 10 most frequent words in the description of all the collected repositories since the start of the streaming application and the number of occurrences of each word, sorted from the most frequent to the least, for each of the three programming languages in real-time. The lists are updated every 60 seconds.
