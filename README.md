# JPedal Docker Image #

JPedal is a Java PDF library for converting, extraction, viewing and printing PDF documents. This docker image can be used to containerise JPedal making its image/text extraction and PDF to image conversion functionality accessible via a REST API which is perfect for cloud deployments.

## Getting Started ##

In order to use the JPedal Docker image you will need a license to access the JPedal war file. If you have not got a license yet, you can [sign up for a free trial](https://www.idrsolutions.com/jpedal/trial-download).

Once you have the JPedal war file, you can pull and run the docker image with the following commands:
```bash
docker pull idrsolutions/jpedal:latest
docker run -p 80:80 --mount "source=/path/to/war/jpedal-microservice.war,target=/usr/local/tomcat/webapps/ROOT.war,type=bind" idrsolutions/jpedal
```
A full tutorial with additional options can be [found here](https://support.idrsolutions.com/jpedal/tutorials/cloud/docker/deploy-jpedal-on-docker).

## Building the Image ##

To build the image from the source use the following steps.

- Clone the project from [here](https://github.com/idrsolutions/jpedal-docker)
- Navigate to the project directory in a terminal
- Run the following command  
  ```docker build -t idrsolutions/jpedal .```

## Documentation ## 

[JPedal Cloud Documentation](https://support.idrsolutions.com/jpedal/tutorials/cloud/)
[JPedal Docker Documentation](https://support.idrsolutions.com/jpedal/tutorials/cloud/docker)
[Contact IDRsolutions](https://www.idrsolutions.com/contact-us)