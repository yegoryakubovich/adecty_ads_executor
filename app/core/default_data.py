from database.models import SettingTypes

shops_list = [{'name': 'no name'}]

settings_list = [
    {
        'name': 'URL для тестирования прокси', 'key': 'proxy_check_url',
        'type': SettingTypes.string, 'value': 'https://ifconfig.me/all.json'
    },
    {
        'name': 'Сон новой сессии (сек)', 'key': 'new_session_sleep',
        'type': SettingTypes.num, 'value': '3600'},
    {
        'name': 'Минимальный сон между задачами (сек)', 'key': 'session_sleep_min',
        'type': SettingTypes.num, 'value': '600'
    },
    {
        'name': 'Максимальный сон между задачами (сек)', 'key': 'session_sleep_max',
        'type': SettingTypes.num, 'value': '900'
    },
    {
        'name': 'Сон между проверкой сообщений (сек)', 'key': 'session_answer_sleep',
        'type': SettingTypes.num, 'value': '300'
    },
    {
        'name': 'Сон ассистента долгий (сек)', 'key': 'assistant_sleep',
        'type': SettingTypes.num, 'value': '900'
    },
    {
        'name': 'Сон ассистента долгий (сек)', 'key': 'assistant_sleep_rarely',
        'type': SettingTypes.num, 'value': '3600'
    },
    {
        'name': 'Максимальное количество задач', 'key': 'session_task_max',
        'type': SettingTypes.num, 'value': '15'
    },
    {
        'name': 'Количество сообщений между постами', 'key': 'send_message_delay',
        'type': SettingTypes.num, 'value': '30'
    },
    {
        'name': 'Ключевые слова для добавления пользователей (запятая)', 'key': 'user_save_key_word',
        'type': SettingTypes.list, 'value': 'обмен,обменник'
    },
    {
        'name': 'Обновление статистики присутствия (сек)', 'key': 'group_presence_delay',
        'type': SettingTypes.num, 'value': '300'
    },


]

groups_list = (
    "kekajangroup", "adaptaciyausa", "adaptaciya_ua_usa", "ads_new_york", "calosangeles", "ca_miami_chat",
    "chatamerika", "chatinnj", "chatinSeattle", "chatinsf", "chatnewyork1", "chchatua", "chicagoil", "la_services",
    "losangeles2021immigrants", "los_angeles_avito", "los_angeles_ca", "los_angeles_california_usa", "miamichatik",
    "miamichatru", "movingsf", "multinational_group", "nashaphiladelphia", "nashlosangeles", "nashmiami", "nashny",
    "newyorkchatru", "nyjobsusa", "philadelphiachat", "phillychat", "russianlo", "sacramentocity", "telemarketus",
    "ukrnewyorkgroup", "usachatru", "usaforuz", "usagreen", "usarmenians", "usa_360", "usb_mexico_usa",
    "uzbeksinusalup", "vatandoshimuzbus", "vatandoshim_usa_50_state", "vatandoshim_uz", "vatandoshimusa",
    "yagonadarchausany", "nomadsfamilyusa", "kg_america", "nashchicago", "nomadschicago", "sfnomad",
    "mahallanewyorkjobs", "nomadssd", "mexicousa21", "newyorknash1", "rentcarnomad", "rusoenmexico", "workersnomads",
    "ads_california", "america_new_york", "canada_work_life", "creditmebel908203131", "dogbanusa", "freeshipping",
    "horizont24", "housingnomad", "jobinmoving", "jobs_usa24", "jobsinny", "la_california", "liveintheusa", "mextous",
    "miamihotchat", "nomadsboston", "nomadsmiami", "nomadsdc", "nomadsfamily", "poputchiki_usa", "rent_miami_rusrek",
    "russianclassifieds", "teachbkusa", "trucker_cargo", "usa_benefit", "usa_exchange", "usa_job_help",
    "usa_job_helper", "usamexico", "used21cars", "biznesdvigusa", "miamiarea", "newyorkchat24", "newyork_job", "vhi7f",
    "mayami_360", "nomadsfamilyla", "nyjobs_usa", "in_miami", "los_angeles_cal", "LosAngeleschat_ru", "LA_biznes",
    "Los_Angeles_california_usa", "LosAngeles_life", "LosAngelesInfo", "NashLosAngeles", "LAForum24",
    "losangelesfriends", "Los_Angeles_CA", "losangelesdayru", "la_mycity", "Los_Angeles_PrivateClub", "russianlo",
    "jobs1nLA", "Rent_Los_Angeles_RusRek", "olxla1", "los_angeles_LA", "California_ru", "LA_services",
    "multinational_group", "la_helps", "la_chat_ru", "LosAngeles_Go", "Chat_Work_Los_Angeles", "los_work",
    "CALosAngeles", "Los_angeles_avito", "Los_Angeles_Reklama", "la_chat_work", "LAchatik", "kvartira_new_york",
    "renthouselup", "NewYork_Go_Travel", "kvartirnii_vopros_NY", "new_york_citychat", "ads_new_york", "nyjobsusa",
    "ukrnewyorkgroup", "NYchatik", "newyorkfriend", "svoiny", "NewYork_info", "ChatNewYork1", "rentinNewYokkChat",
    "new_york_avito", "Ukraine_in_USA", "NYCmarket", "Gorodskoy_chat_NY", "JobsInNewYork", "NashNY", "Nyjobs_usa",
    "usaforuz", "NewYorkNash1", "sportmiami", "miami_livechat", "MiamiChatik", "MIAMI_HELP", "maiami_are",
    "Miami_Avito_Go", "gorodskoy_chat_miami", "Miami_GoTravel", "miamskiyydvizh", "ours_chat_miami2",
    "MiamiFloridainfo", "miami_helps", "miamired", "miami_services", "miamiarea", "miamifriends", "miami_chat_rus",
    "Miami_avito", "businessMiamii", "CA_Miami_Chat", "NashMiami", "gorodskoy_chat_miami", "Jobs1nChicago",
    "BazMeetChicago", "rentinChicagoChat", "Obshchaya_Sbor_Chikago", "ChicagoIL", "chired", "CHchatUA", "NashChicago",
    "chicago_avito", "chicagoass", "jobs1nSeattle", "Seattle_avito", "seattlered", "rentinSiettleChat",
    "businessSiettle", "sacramentocity", "SacramentoinChat", "businessSacrament0", "ctatinSacramento",
    "rentinSacramentoChat", "sacramentored", "adaptationinsacramento", "cNecRg9IeLlkNmUx", "Washington_life", "usa_360",
    "Obmenik_USA", "UsaExchangeChat", "exchange_chat_usa", "usb_mexico_usa", "dhdhdhfhfhfh", "VATANDOSHIM_USA_50_state",
    "uzbeksinusalup", "YagonadarchausaNY", "VatandoshimYGU", "chatamerika", "ours_app", "vatandoshimuzbus",
    "Vatandoshim_uz", "pets_delivery_usa_europe_canada", "chatamericaUA", "biznesdvigusa", "Poruchiteli", "Horizont24",
    "dogbanusa", "americaindetails", "poputchiki_usa", "adaptaciya_UA_USA", "mahallanewyorkjobs", "usa_benefit",
    "poruschitel", "USA_job_helper", "USA_job_help", "YagonadarchausaNY", "usamexico", "USACHATRU", "mexicoUSA21",
    "Works_usa", "UZimiznikilarCOM", "jobs_usa24", "nomadsfamilyusa", "chatinSF", "chat_rusrek_sanfrancisco",
    "san_francisco_avito", "jobsinSF", "rentinSanFranciscoChat", "SanFranciscoinChat", "businessSanFrancisco",
    "WorldCalifornia", "NashaPhiladelphia", "philadelphiafriends", "Chat_Philadelphia_RusRek",
    "philadelpia_pennsylvania", "rentinPhiladelphiaChat", "businessPhiladelphia", "Philadelphiachat", "phillychat",
    "chatinNJ", "BazMeetNewJersey", "businessNewJersey", "chicagoil", "chicagochatik", "russianlo", "los_angeles_ca",
    "los_angeles_avito", "los_angeles_california_usa", "multinational_group", "los_angeles3", "LA_services",
    "NashLosAngeles", "LAchatik", "NashMiami", "MIAMICHATRU", "CA_Miami_Chat", "MiamiChatik", "ChatNewYork1",
    "NYchatik", "CALosAngeles", "NEWYORKCHATRU", "ads_new_york", "usagreen", "usaforuz", "forum_usa", "usa_360",
    "chatamerika", "vatandoshimuzbus", "YagonadarchausaNY", "usb_mexico_usa", "telemarketus", "uzbeksinusalup",
    "renthouselup", "CHchatUA", "phillychat", "NashaPhiladelphia", "Philadelphiachat", "ukrnewyorkgroup", "chatinNJ",
    "movingSF", "chatinSF", "adaptationinsacramento", "sacramentocity", "adaptaciyaUSA", "ponaehali_USA",
    "adaptaciya_UA_USA", "russian_seattle", "chatinSeattle", "NashNY", "Vatandoshim_uz", "USACHATRU",
    "gofortravel_chat", "usarmenians", "nyjobsusa", "VATANDOSHIM_USA_50_state", "vatandoshlaa", "adaptaciya_ua_usa",
    "adaptaciyausa", "adaptationinny", "adaptationinsacramento", "ads_california", "ads_new_york", "america_new_york",
    "askomain", "avitomiami", "biznesdvigusa", "britishcolambia", "brooklynnewyorkjob", "bwfull", "ca_miami_chat",
    "california_los_angeles1", "california_russian", "california123", "californiaads", "californiajob",
    "californiarabota", "californiareklama", "calosangeles", "canada_work_life", "chatamerika", "chatinnj",
    "chatinSeattle", "chatinsf", "chatnewyork1", "chchatua", "chicagochatik", "chicagoil", "creditmebel908203131",
    "darom_ny", "dogbanusa", "forum_usa", "freeshipping", "gofortravel_chat", "horizont24", "housingnomad", "in_miami",
    "jobinmoving", "jobs_usa24", "jobsinny", "kg_america", "la_california", "la_services", "lachatik", "liveintheusa",
    "los_angeles_avito", "los_angeles_ca", "los_angeles_california_usa", "losangeles2021immigrants",
    "mahallanewyorkjobs", "mayami_360", "mexicochatik", "mexicousa21", "mextous", "miamiarea", "miamiavito",
    "miamichatik", "miamichatru", "miamihotchat", "movingsf", "multinational_group", "nashaphiladelphia", "nashchicago",
    "nashlosangeles", "nashmiami", "nashny", "newyork_job", "newyorkchat24", "newyorkchatru", "newyorknash1",
    "nomadsboston", "nomadschicago", "nomadsdc", "nomadsfamily", "nomadsfamilyla", "nomadsfamilyusa", "nomadsmiami",
    "nomadssd", "nychatik", "nyjobs_usa", "nyjobsusa", "philadelphiachat", "phillychat", "ponaehali_usa",
    "poputchiki_usa", "rent_miami_rusrek", "rentcarnomad", "renthouselup", "rusoenmexico", "russian_seattle",
    "russianclassifieds", "russianlo", "sacramentocity", "sfnomad", "skyyogahollywoodfl", "teachbkusa", "telemarketus",
    "trucker_cargo", "ukrnewyorkgroup", "usa_360", "usa_benefit", "usa_exchange", "usa_job_help", "usa_job_helper",
    "usachatru", "usaforuz", "usagreen", "usamexico", "usarmenians", "usb_mexico_usa", "used21cars", "uzbeksinusalup",
    "vatandoshim_usa_50_state", "vatandoshim_uz", "vatandoshimusa", "vatandoshimuzbus", "vhi7f", "vhi7fvhi7f",
    "workersnomads", "yagonadarchausany",

    "avtorynok_moskva", "avtorynok_rossias", "perekupavtoRF", "avtoprov", "tatarstan_avtorynok", "avtozapret_avito_net",
    "avtourala", "avtobazar_dnepr", "avtorynok_ekaterinburg", "auto_irkutska", "autobmg", "avtomobili_nn",
    "vadimavtopodborr", "zherdesh", "avto_kurs_chat", "easycartatarstan", "autozapchasti_ru", "avtomobili_russia",
    "avtobaraholkaa", "autorynokkzn", "autotrade77", "phuket_arenda", "columbchat", "avtorynok_omsk_55",
    "avtorynok_omska", "dorogachat", "pattaya_arenda", "avto_iz_germanii_gtk", "kznavto16", "zapchasti_chat1",
    "avtorynok_Russian", "megadriveru", "avtoxak42", "avtotemaav", "dpsoblava", "avtopomoshlnr", "rf_avtorinok",
    "auto_mrpl", "logistics_avto", "avtorynok_kg_iqro", "spectehno", "autobykzn", "avtosalerussia", "telega_cart",

    "chinaforbiz", "enmotor", "wbchat_wb", "deliveryland", "yabaolu", "x_delivery", "cargochinachat", "mpgroup_china",
    "china_russia_ff", "expresschina28", "sellerkellerfulf", "logistics_china", "cargo1one", "kargoh", "milafbruchat",
    "kargo352", "businesswithchina2022", "quicktao_cargo1", "antmineropt", "marketroi", "dostavkakargo",
    "avaslogistics", "cargo5566", "china_zakup", "russian1688", "milafbruchat2", "chinamocow", "magneskitay",
    "logistics_china_kz", "flgchina", "el_motorscom", "fulfilment4", "Batareyka125rus", "joycity_chat",
    "cargo8866dostavkaot10kg", "cargoizchina", "tovarka_kitay_chat", "getabox_china_chat", "travel_chat_rus1",
    "aaalogistics_chat", "cargo889_leva", "unclemaochat", "dalex_chat", "cargogroup", "topcar_chat", "miner_bros",

)

surnames_man = [
    "Ivanov", "Smirnov", "Kuznetsov", "Popov", "Vasiliev", "Petrov", "Sokolov", "Mikhailov", "Novikov", "Fedorov",
    "Morozov", "Volkov", "Alekseev", "Lebedev", "Semenov", "Egorov", "Pavlov", "Kozlov", "Stepanov", "Nikolaev",
    "Orlov", "Andreev", "Makarov", "Nikitin", "Zakharov", "Zaitsev", "Soloviev", "Borisov", "Yakovlev", "Grigoriev",
    "Romanov", "Vorobiev", "Sergeev", "Kuzmin", "Frolov", "Alexandrov", "Dmitriev", "Korolev", "Gusev", "Kiselev",
    "Ilyin", "Maximov", "Polyakov", "Sorokin", "Vinogradov", "Kovalev", "Belov", "Medvedev", "Antonov", "Tarasov",
    "Zhukov", "Baranov", "Filippov", "Komarov", "Davydov", "Belyaev", "Gerasimov", "Bogdanov", "Osipov", "Sidorov",
    "Matveev", "Titov", "Markov", "Mironov", "Krylov", "Kulikov", "Karpov", "Vlasov", "Melnikov", "Denisov", "Gavrilov",
    "Tikhonov", "Kazakov", "Afanasiev", "Danilov", "Saveliev", "Timofeev", "Fomin", "Chernov", "Abramov", "Martynov",
    "Efimov", "Fedotov", "Shcherbakov", "Nazarov", "Kalinin", "Isaev", "Chernyshev", "Bulls", "Maslov", "Rodionov",
    "Konovalov", "Lazarev", "Voronin", "Klimov", "Filatov", "Ponomarev", "Golubev", "Kudryavtsev", "Prokhorov",
    "Naumov", "Potapov", "Zhuravlev", "Ovchinnikov", "Trofimov", "Leonov", "Sobolev", "Ermakov", "Kolesnikov",
    "Goncharov", "Yemelyanov", "Nikiforov", "Grachev", "Kotov", "Grishin", "Efremov", "Arkhipov", "Gromov", "Kirillov",
    "Malyshev", "Panov", "Moiseev", "Rumyantsev", "Akimov", "Kondratiev", "Biryukov", "Gorbunov", "Anisimov", "Eremin",
    "Tikhomirov", "Galkin", "Lukyanov", "Mikheev", "Skvortsov", "Yudin", "Belousov", "Nesterov", "Simonov", "Prokofiev",
    "Kharitonov", "Knyazev", "Tsvetkov", "Levin", "Mitrofanov", "Voronov", "Aksenov", "Sofronov", "Maltsev", "Loginov",
    "Gorshkov", "Express"

]
surnames_woman = [
    "Ivanova", "Smirnova", "Kuznetsova", "Popova", "Vasilieva", "Petrova", "Sokolova", "Mikhailovna", "Novikovna",
    "Fedorova", "Morozova", "Volkova", "Alekseeva", "Lebedeva", "Semenova", "Egorova", "Pavlova", "Kozlova",
    "Stepanova", "Nikolaeva", "Orlova", "Andreeva", "Makarova", "Nikitina", "Zakharova", "Zaitseva", "Solovieva",
    "Borisova", "Yakovleva", "Grigorieva", "Romanova", "Vorobieva", "Sergeeva", "Kuzmina", "Frolova", "Alexandrova",
    "Dmitrieva", "Koroleva", "Guseva", "Kiseleva", "Ilyina", "Maximova", "Polyakova", "Sorokina", "Vinogradova",
    "Kovaleva", "Belova", "Medvedeva", "Antonova", "Tarasova", "Zhukova", "Baranov", "Filippov", "Komarov", "Davydov",
    "Belyaev", "Gerasimov", "Bogdanov", "Osipov", "Sidorova", "Matveeva", "Titova", "Markova", "Mironova", "Krylova",
    "Kulikova", "Karpova", "Vlasova", "Melnikova", "Denisova", "Gavrilova", "Tikhonova", "Kazakova", "Afanasieva",
    "Danilova", "Savelieva", "Timofeeva", "Fomina", "Chernova", "Abramova", "Martynova", "Efimova", "Fedotova",
    "Shcherbakova", "Nazarova", "Kalinina", "Isaeva", "Chernysheva", "Bullsa", "Maslova", "Rodionova", "Konovalova",
    "Lazareva", "Voronina", "Klimova", "Filatova", "Ponomareva", "Golubeva", "Kudryavtseva", "Prokhorova", "Naumova",
    "Potapova", "Zhuravleva", "Ovchinnikova", "Trofimova", "Leonova", "Soboleva", "Ermakova", "Kolesnikova",
    "Goncharova", "Yemelyanova", "Nikiforova", "Gracheva", "Kotova", "Grishina", "Efremova", "Arkhipova", "Gromova",
    "Kirillova", "Malysheva", "Panova", "Moiseeva", "Rumyantseva", "Akimova", "Kondratieva", "Biryukova", "Gorbunova",
    "Anisimova", "Eremina", "Tikhomirova", "Galkina", "Lukyanova", "Mikheeva", "Skvortsova", "Yudina", "Belousova",
    "Nesterova", "Simonova", "Prokofieva", "Kharitonova", "Knyazeva", "Tsvetkova", "Levina", "Mitrofanova", "Voronova",
    "Aksenova", "Sofronova", "Maltseva", "Loginova", "Gorshkova", "Express"
]

names_man = [
    "Alexander", "Mikhail", "Kirill", "Aleksey", "Victor", "Denis", "Dmitry", "Daniel", "Matvey", "Gregory", "Ilya",
    "Maxim", "Andrey ", "Yaroslav", "Vladimir", "Timofey", "Timur", "Eugene", "Vasily", "Sergei", "Platon", "Ivan",
    "Arseny", "Damir", "Roman", "Artem", "Egor", "Lev", "Stepan", "Robert", "Bogdan", "Miron", "Erik", "Nikita", "Gleb",
    "Stanislav", "Vladislav", "Arthur ", "Anton", "Igor", "Savely", "Mstislav", "Nazar", "Zakhar", "Leonid", "David",
    "Gennady", "Elizar", "Konstantin", "Vsevolod", "Finance"
]
names_woman = [
    "Avdotya", "Agafya", "Aglaya", "Agnessa", "Agrafena", "Agripina", "Adelaida", "Aksinya", "Akulina", "Aleksandra",
    "Aleksandrina", "Alena", "Alesha", "Alina", "Alisa", "Alla", "Albina", "Alma", "Anastasiya", "Anzhela", "Anzhelina",
    "Anna", "Antonida", "Antonina", "Antoniya", "Anfisa", "Apollinariya", "Arina", "Astra", "Asya", "Afanasiya",
    "Valeriya", "Varvara", "Vasilisa", "Vasya", "Velimira", "Vera", "Veronika", "Viktoriya", "Vilena", "Vitoslava",
    "Vladilena", "Vladlena", "Vyacheslava", "Gavriila", "Gavrila", "Gala", "Galina", "Gena", "Gertrud", "Glafira",
    "Gordeya", "Gorimira", "Gradimira", "Gradislava", "Granislava", "Grunya", "Grusha", "Gulya", "Darya", "Dekabrina",
    "Denis", "Dima", "Dobrodeya", "Dobromila", "Dobromira", "Dobroslava", "Dolyana", "Dragomila", "Dragoslava", "Dunya",
    "Eva", "Evgeniya", "Evdokiya", "Evpraksiya", "Ekaterina", "Elena", "Elizaveta", "Emelya", "Esfir", "Efimiya",
    "Efrosinya", "Zhanna", "Zabava", "Zarina", "Zarya", "Zvenimira", "Zinaida", "Zoya", "Ivanna", "Izyaslava", "Inna",
    "Iolanta", "Irina", "Isidora", "Iskra", "Kapeka", "Karina", "Katerina", "Katya", "Kim", "Kira", "Klavdiya", "Klara",
    "Krasava", "Ksana", "Kseniya", "Kuksha", "Kupava", "Lana", "Larisa", "Lelya", "Lena", "Lenara", "Leniana", "Lenina",
    "Lenya", "Leon", "Lidiya", "Liza", "Lizaveta", "Liliya", "Lora", "Lukeriya", "Lukerya", "Luchezara", "Lyubov",
    "Lyudmila", "Magdalina", "Manya", "Margarita", "Marianna", "Marina", "Mariya", "Marlena", "Marfa", "Marya",
    "Maryamna", "Matrena", "Matrona", "Masha", "Mina", "Nadezhda", "Nayda", "Nastasya", "Nastya", "Nataliya", "Nika",
    "Nina", "Ninella", "Ninel", "Nona", "Nonna", "Oksana", "Oktyabrina", "Olelya", "Olga", "Olya", "Ostromira",
    "Ostroslava", "Otrada", "Pelageya", "Polina", "Pravdina", "Praskovya", "Prekrasa", "Rada", "Radinka", "Radomira",
    "Radoslava", "Raisa", "Ratimira", "Revmira", "Rimma", "Roza", "Roksana", "Rusya", "Rufina", "Sanya", "Sasha",
    "Sveta", "Svetlana", "Svoboda", "Serafima", "Sivilla", "Slava", "Slaviya", "Smeyana", "Sofiya", "Sofya", "Stasya",
    "Sudislava", "Syuzanna", "Taisiya", "Tamara", "Tatyana", "Tasha", "Tverdimira", "Tverdislava", "Tina", "Tosha",
    "Ulyana", "Ustinya", "Faina", "Fekla", "Feklista", "Feodora", "Filippa", "Foka", "Shura", "Yuliana", "Yuliya",
    "Yura", "Yustina", "Yan", "Yara", "Yarina", "Yaromira", "Yaroslava", "Finance"
]

about_unisex = [
    "TG: @fexps_obmen"
]

avatars_man = [f"man_{i + 1}.jpg" for i in range(26)] + ["fexps.jpg"]
avatars_woman = [f"woman_{i + 1}.jpg" for i in range(34)] + ["fexps.jpg"]
avatars_unisex = [f"woman_{i + 1}.jpg" for i in range(4)] + ["fexps.jpg"]
