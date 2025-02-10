### Frontend server
npm run dev


### todo
- typing
- fix bug with read message send by me
- chats design отображения времени + даты - userchat - gif display, video - muted + timer, fullscreen images + video
- design right section
- v-auto-animate options
- color pics for chats + api
- reseize cahts + api
- открытия роуты в aside + закрытие сокетов onUnmount
- перманентный кеш
- тосты на новое сообщение если роут не /messages + отображения пользователя при нажатии делаем редирект начат, если от websocket делаем просто редирект на /messages + отображение пользователя и сообщение
- тест нагрузку на цп + потребление памяти
- перейти в чат -> редирект на кеш и выбор чата + тест непрочитанных сообщений + отображения онлайна
- новый чат редирект создать чат + сокет соединения + сделать load чата + тест прочитанных + тест онлайна
- userview новый чат меняем на перейти в чат + тестируем


### Easy
- all pins hover buttons better
- user view change tab animations
- search home view animations
- back arrow better design
- pin detail buttons scale on hover
- v-auto-animate options


### Medium
- emoji for every input
- home search design
- not found design
- иконки везде пиздатые сделать
- fix add coment input on same file handle
- login/signup purple?
- video controls animation?
- like comment animation from icon
- truncate title, description pin detail


### Hard
- pins desc order
- notauth page scrolling + describe all functional - https://codepen.io/rexjbull/pen/RwRRezq
- after save pin - анимацию что пин сохранен
- pin detail, play comments video + controls
- play tags video after back
- tags стрелочки показываем или нет
- tags without pins dont show
- tags sort
- tags pagination home/create
- create pin url load
- create pin - multiply files
- user view - display messages for me/other user if no pins
- change font
- loaders for userview
- loaders for not-found
- rewrite all img/video loaders
- delete saved pin / delete created pin - modal are u sure with preview of pin
- chatgpt for impove all components
- after user create pin in home show animation
- везде где пагинацию - обратная отдача
- create pin loader
- create pin max-height
- rgb на коменты и профили пользователей + свечение везде
- pin detail на загрузку без прыжков
- fix video play after reload detail, after back - comments, controls + preview - controls, play after back
- keep alive optimization
- home optimization videos
- pin detail optimization
- toasts need or no ?
- pin detail likes full screen
- all full screen close by esc or click on overlay
- fix errors in userpopout
- show only 1 reply
- pin detail - image - show full screen image/video + analyze pinterest detail, add button for link
- all likes show by lick on full screen
- userpopout display over section + top/bottom displayed
- delete comment/edit
- user view design (after fix verification + user to user api)
  - toasts for update profile and why dont updated?????
- user can disable add comment on pin
- reply in replies
- test all axios for inputs server error for all requests - toasts
  - test all inputs for trim(), errors
- edit user email + verification + edit old verification refactor
- updates
 - schedule reklama
 - updates from another users interation
- direct messages
 - every user can write message to another user
 - dialog display in /messages
- add boards
- add черновики 
- after create pin - celery + celery results + notification for user
- analyze pinterest to add more functions, awesome vuejs



- https://github.com/amineyarman/vue-kinesis
- https://github.com/vuejs/awesome-vue
- https://codepen.io/rexjbull/pen/RwRRezq
- https://codepen.io/andymerskin/pen/XNMWvQ