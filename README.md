# amo_api
тестовое для nova

конфигурация:

заменить .env.template на .env и заполнить

получить access и refresh токены и добавить в бд через админку
![add_token](readme_pics/add_token.png)

эндпонт для get запроса:
/api/amo/

можно затестить онлайн:

[heroku](https://amo-api-test.herokuapp.com/)

пример запроса(можно просто скопировать в адр строку браузера, заменив параметры):

https://amo-api-test.herokuapp.com/api/amo/?email=testmail@mail.ru&name=testname&phone=+79963416438
