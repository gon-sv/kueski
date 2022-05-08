## kueski
challenge de kueski

# pipeline de consumo

![Flowchart](https://user-images.githubusercontent.com/10265468/167302800-077e84d3-af94-41ac-9366-f68fca2109a7.jpg)

A1- el usuario envia un request a la funcion lambda "reques handler"

A2- el request es enviado con un traceID a un queue SQS, a la cual se le solicita el numero de requests en cola. si este llegara a superar cierto numero predefinido, se hace un pedido a "batch process handler", que recibe el batch de la queue SQS.

A3- "batch process handler" consulta con sagemaker model registry los active endpoints. de haber mas de una version activa, en via un cierto porcentaje (leido de una dynamoDB que no figura en el esquema por simplicidad) a la nurva version yel resto a la version previa. tambie, envia el batch a el baseline.

A4- "batch process handler" anota en una dynamoDB  los traceID, las predicciones junto a la data provista y el modelo al cual se le asigno

A5- "ground truth hanlder" recibe el groundtruth y actualiza la dynamo previa.

A6- "model handler" es activado por una cloudwatch alarm para verificar (en base a los datos de la dynamo) la performance de los modelos activos. esta puede elegir retirar un modelo, incrementar el porcentaje de batch recibido por cada modelo (ramp up) o reducirlo (rollback).

# dentro de sagemaker

B1- en base a los resultados del cloudwatch monitor y sus thresholds definidos, se puede decidir de manera automatica si reentrenar un modelo o retirarlo. tambien, mediante el model monitor podria detectarse drift. este reentrenamiento se lleva a cabo mediante el pipeline esbozado en las notebooks.

![SMPipeline](https://user-images.githubusercontent.com/10265468/167303431-3595a31d-5f28-4625-a63b-7d4d799ebcfd.png)


B2- especialmente en casos de creditos, es importante la transparencia y explicabilidad del modelo, para ello utilizamos sagemaker clarify.

# pipeline de desarrollo

![ML-4030-image001](https://user-images.githubusercontent.com/10265468/167303486-da2b5ef6-35f4-4e7b-9f24-090a21638ef6.jpg)






