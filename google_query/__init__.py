# -*-coding: utf-8 -*-
import urllib


class GoogleQuery():

    base_url_tpl = 'https://www.google.{zone}/search?q={query}{params}'

    zone_params = {
        'com.ua': {
            'hl': 'ru'
        },
        'co.uk': {
            'hl': 'en'
        },
        'co.id': {
            'hl': 'en',
            'custom': 'gl=en'
        },
        'com.hk': {
            'hl': 'en',
            'custom': 'gl=en&pws=0&gcs=Hongkong'
        },
        'bg': {
            'hl': 'bg'
        },
        'com.uag': {
            'hl': 'ru',
            'custom': 'tbs=ctr:countryUA&cr=countryUA'
        },
        'com': {
            'hl': 'en',
            'custom': 'gl=US&gr=US-UT&gcs=NewYork'
        }
    }

    num = 10

    regions_coords = {u'черкесск': {u'latitude': u'442273974', u'longitude': u'420591708'}, u'донецк': {u'latitude': u'480158829', u'longitude': u'378028500'}, u'златоуст': {u'latitude': u'551558786', u'longitude': u'596858852'}, u'нидерланды': {u'latitude': u'521326330', u'longitude': u'52912659'}, u'первоуральск': {u'latitude': u'568999157', u'longitude': u'599521127'}, u'швеция': {u'latitude': u'601281610', u'longitude': u'186435010'}, u'соликамск': {u'latitude': u'596720331', u'longitude': u'567557667'}, u'талдыкорган': {u'latitude': u'450177112', u'longitude': u'783804416'}, u'норвегия': {u'latitude': u'604720240', u'longitude': u'84689459'}, u'таджикистан': {u'latitude': u'388610340', u'longitude': u'712760930'}, u'таиланд': {u'latitude': u'158700320', u'longitude': u'1009925409'}, u'воронеж': {u'latitude': u'516754965', u'longitude': u'392088823'}, u'мытищи': {u'latitude': u'559198471', u'longitude': u'377654985'}, u'швейцария': {u'latitude': u'468181880', u'longitude': u'82275119'}, u'каменск-уральский': {u'latitude': u'564253389', u'longitude': u'619222979'}, u'тверь': {u'latitude': u'568587214', u'longitude': u'359175965'}, u'зеленоград': {u'latitude': u'557558260', u'longitude': u'376173000'}, u'латвия': {u'latitude': u'568796350', u'longitude': u'246031890'}, u'балаково': {u'latitude': u'520245587', u'longitude': u'477806626'}, u'эстония': {u'latitude': u'585952719', u'longitude': u'250136070'}, u'херсон': {u'latitude': u'466354170', u'longitude': u'326168670'}, u'караганда': {u'latitude': u'498046834', u'longitude': u'731093826'}, u'новомосковск': {u'latitude': u'540109034', u'longitude': u'382963063'}, u'ульяновск': {u'latitude': u'543181598', u'longitude': u'483837914'}, u'смоленск': {u'latitude': u'547903112', u'longitude': u'320503663'}, u'муром': {u'latitude': u'555673975', u'longitude': u'420165852'}, u'барнаул': {u'latitude': u'533547791', u'longitude': u'837697831'}, u'кстово': {u'latitude': u'561328850', u'longitude': u'441740097'}, u'тында': {u'latitude': u'551438334', u'longitude': u'1247413765'}, u'благовещенск': {u'latitude': u'502727763', u'longitude': u'1275404016'}, u'макеевка': {u'latitude': u'480459557', u'longitude': u'379666901'}, u'красноярск': {u'latitude': u'560152833', u'longitude': u'928932476'}, u'ростов': {u'latitude': u'571956230', u'longitude': u'394131527'}, u'новороссийск': {u'latitude': u'447154014', u'longitude': u'377619669'}, u'хорватия': {u'latitude': u'451000000', u'longitude': u'152000000'}, u'алматы': {u'latitude': u'432220146', u'longitude': u'768512485'}, u'озерск': {u'latitude': u'557138099', u'longitude': u'607009592'}, u'новая зеландия': {u'latitude': u'-409005570', u'longitude': u'1748859709'}, u'кострома': {u'latitude': u'577774815', u'longitude': u'409698928'}, u'кемерово': {u'latitude': u'553450231', u'longitude': u'860623044'}, u'апатиты': {u'latitude': u'675777880', u'longitude': u'333904158'}, u'старый оскол': {u'latitude': u'512980824', u'longitude': u'378379593'}, u'франция': {u'latitude': u'462276380', u'longitude': u'22137490'}, u'раменское': {u'latitude': u'555685727', u'longitude': u'382212691'}, u'ржев': {u'latitude': u'562583967', u'longitude': u'343283487'}, u'актобе': {u'latitude': u'502839339', u'longitude': u'571669780'}, u'усть-илимск': {u'latitude': u'579845405', u'longitude': u'1027395955'}, u'калининград': {u'latitude': u'547104263', u'longitude': u'204522144'}, u'назрань': {u'latitude': u'432148800', u'longitude': u'447763500'}, u'анапа': {u'latitude': u'448857007', u'longitude': u'373199191'}, u'гусь-хрустальный': {u'latitude': u'556062836', u'longitude': u'406563727'}, u'уфа': {u'latitude': u'547387620', u'longitude': u'559720553'}, u'нижневартовск': {u'latitude': u'609431185', u'longitude': u'765433724'}, u'петропавловск-камчатский': {u'latitude': u'530409109', u'longitude': u'1586777258'}, u'владимир': {u'latitude': u'561445955', u'longitude': u'404178686'}, u'нижнекамск': {u'latitude': u'556131959', u'longitude': u'518469974'}, u'сан-франциско': {u'latitude': u'377749295', u'longitude': u'-1224194155'}, u'чеченская республика': {u'latitude': u'434023301', u'longitude': u'457187468'}, u'хабаровск': {u'latitude': u'485027313', u'longitude': u'1350662599'}, u'нью-йорк': {u'latitude': u'407127836', u'longitude': u'-740059413'}, u'оренбург': {u'latitude': u'517666482', u'longitude': u'551004538'}, u'бердск': {u'latitude': u'547750638', u'longitude': u'830800316'}, u'солнечногорск': {u'latitude': u'561852039', u'longitude': u'369776170'}, u'норильск': {u'latitude': u'693557900', u'longitude': u'881892938'}, u'турция': {u'latitude': u'389637449', u'longitude': u'352433220'}, u'люберцы': {u'latitude': u'556864620', u'longitude': u'378981554'}, u'нефтекамск': {u'latitude': u'561026081', u'longitude': u'542867393'}, u'африка': {u'latitude': u'-87831950', u'longitude': u'345085230'}, u'черкассы': {u'latitude': u'494444330', u'longitude': u'320597670'}, u'междуреченск': {u'latitude': u'536960514', u'longitude': u'880953241'}, u'чистополь': {u'latitude': u'553617503', u'longitude': u'506338907'}, u'альметьевск': {u'latitude': u'548937127', u'longitude': u'523172930'}, u'алтайский край': {u'latitude': u'517936298', u'longitude': u'826758596'}, u'гомель': {u'latitude': u'524411761', u'longitude': u'309878462'}, u'северодвинск': {u'latitude': u'645661757', u'longitude': u'398505981'}, u'самара': {u'latitude': u'532415041', u'longitude': u'502212463'}, u'москва': {u'latitude': u'557558260', u'longitude': u'376173000'}, u'харьков': {u'latitude': u'499935000', u'longitude': u'362303829'}, u'канада': {u'latitude': u'561303659', u'longitude': u'-1063467709'}, u'петрозаводск': {u'latitude': u'617781617', u'longitude': u'343640396'}, u'полтава': {u'latitude': u'495882669', u'longitude': u'345514170'}, u'жигулевск': {u'latitude': u'533907252', u'longitude': u'494722694'}, u'челябинск': {u'latitude': u'551644419', u'longitude': u'614368431'}, u'каменск-шахтинский': {u'latitude': u'483102990', u'longitude': u'402445448'}, u'саратов': {u'latitude': u'515563789', u'longitude': u'459798167'}, u'берлин': {u'latitude': u'525200065', u'longitude': u'134049540'}, u'абхазия': {u'latitude': u'423154070', u'longitude': u'433568919'}, u'великие луки': {u'latitude': u'563396088', u'longitude': u'305314750'}, u'ногинск': {u'latitude': u'558761163', u'longitude': u'384666594'}, u'туркмения': {u'latitude': u'389697190', u'longitude': u'595562780'}, u'брест': {u'latitude': u'520976213', u'longitude': u'237340503'}, u'ейск': {u'latitude': u'466825784', u'longitude': u'382702941'}, u'сатка': {u'latitude': u'550467481', u'longitude': u'590082549'}, u'курган': {u'latitude': u'554649113', u'longitude': u'653053512'}, u'прокопьевск': {u'latitude': u'538887529', u'longitude': u'867591829'}, u'хмельницкий': {u'latitude': u'494229829', u'longitude': u'269871330'}, u'житомир': {u'latitude': u'502546500', u'longitude': u'286586669'}, u'коломна': {u'latitude': u'550937517', u'longitude': u'387688617'}, u'рубцовск': {u'latitude': u'515140399', u'longitude': u'812317683'}, u'магадан': {u'latitude': u'595611525', u'longitude': u'1508301412'}, u'мелитополь': {u'latitude': u'468550216', u'longitude': u'353586996'}, u'беларусь': {u'latitude': u'537098070', u'longitude': u'279533889'}, u'сибирь': {u'latitude': u'550083525', u'longitude': u'829357327'}, u'екатеринбург': {u'latitude': u'568389260', u'longitude': u'606057025'}, u'рыбинск': {u'latitude': u'580574860', u'longitude': u'388116968'}, u'волгоград': {u'latitude': u'487080480', u'longitude': u'445133034'}, u'астана': {u'latitude': u'511605226', u'longitude': u'714703558'}, u'гродно': {u'latitude': u'536693537', u'longitude': u'238131305'}, u'димитровград': {u'latitude': u'542269791', u'longitude': u'495684572'}, u'луцк': {u'latitude': u'507472329', u'longitude': u'253253830'}, u'железнодорожный': {u'latitude': u'557373756', u'longitude': u'380095391'}, u'республика хакасия': {u'latitude': u'530452280', u'longitude': u'903982145'}, u'кременчуг': {u'latitude': u'490657829', u'longitude': u'334100330'}, u'троицк': {u'latitude': u'554872242', u'longitude': u'373046546'}, u'гатчина': {u'latitude': u'595624627', u'longitude': u'301064659'}, u'комсомольск-на-амуре': {u'latitude': u'505670330', u'longitude': u'1369658947'}, u'домодедово': {u'latitude': u'557702011', u'longitude': u'376024752'}, u'балашиха': {u'latitude': u'557981903', u'longitude': u'379679867'}, u'словакия': {u'latitude': u'486690259', u'longitude': u'196990239'}, u'новокузнецк': {u'latitude': u'537595934', u'longitude': u'871215704'}, u'тюмень': {u'latitude': u'571612974', u'longitude': u'655250172'}, u'санкт-петербург': {u'latitude': u'599342801', u'longitude': u'303350986'}, u'ялта': {u'latitude': u'444952050', u'longitude': u'341663010'}, u'ханты-мансийск': {u'latitude': u'610090918', u'longitude': u'690374595'}, u'александров': {u'latitude': u'563947309', u'longitude': u'387120369'}, u'чехия': {u'latitude': u'498174919', u'longitude': u'154729619'}, u'финляндия': {u'latitude': u'619241100', u'longitude': u'257481510'}, u'днепропетровск': {u'latitude': u'484647170', u'longitude': u'350461830'}, u'стерлитамак': {u'latitude': u'536554353', u'longitude': u'559438932'}, u'белгород': {u'latitude': u'505997134', u'longitude': u'365982621'}, u'саров': {u'latitude': u'549342792', u'longitude': u'433252503'}, u'ессентуки': {u'latitude': u'440455120', u'longitude': u'428575231'}, u'ковров': {u'latitude': u'563567690', u'longitude': u'413226310'}, u'новоуральск': {u'latitude': u'572575238', u'longitude': u'600834488'}, u'витебск': {u'latitude': u'551848060', u'longitude': u'302016219'}, u'армения': {u'latitude': u'400690990', u'longitude': u'450381889'}, u'сергиев посад': {u'latitude': u'563242317', u'longitude': u'381452114'}, u'бугульма': {u'latitude': u'545220313', u'longitude': u'528260804'}, u'наро-фоминск': {u'latitude': u'553916240', u'longitude': u'367249432'}, u'краматорск': {u'latitude': u'487389669', u'longitude': u'375843500'}, u'переславль': {u'latitude': u'567470480', u'longitude': u'388902603'}, u'кайеркан': {u'latitude': u'693666669', u'longitude': u'877333330'}, u'пермь': {u'latitude': u'580296813', u'longitude': u'562667916'}, u'дмитров': {u'latitude': u'563427702', u'longitude': u'375288416'}, u'севастополь': {u'latitude': u'446166500', u'longitude': u'335253669'}, u'ставрополь': {u'latitude': u'450454764', u'longitude': u'419683431'}, u'иваново': {u'latitude': u'570050671', u'longitude': u'409766453'}, u'корея': {u'latitude': u'359077570', u'longitude': u'1277669220'}, u'усть-каменогорск': {u'latitude': u'499749294', u'longitude': u'826017244'}, u'тель-авив': {u'latitude': u'320852998', u'longitude': u'347817675'}, u'сургут': {u'latitude': u'612559502', u'longitude': u'733845470'}, u'йошкар-ола': {u'latitude': u'566402225', u'longitude': u'478838580'}, u'тернополь': {u'latitude': u'495535170', u'longitude': u'255947669'}, u'болгария': {u'latitude': u'427338830', u'longitude': u'254858300'}, u'одинцово': {u'latitude': u'556733744', u'longitude': u'372818569'}, u'запорожье': {u'latitude': u'478388000', u'longitude': u'351395670'}, u'орел': {u'latitude': u'529668468', u'longitude': u'360624898'}, u'подольск': {u'latitude': u'554312453', u'longitude': u'375457647'}, u'дания': {u'latitude': u'562639200', u'longitude': u'95017850'}, u'ярославль': {u'latitude': u'576260744', u'longitude': u'398844707'}, u'череповец': {u'latitude': u'591323329', u'longitude': u'379091811'}, u'одесса': {u'latitude': u'464825260', u'longitude': u'307233095'}, u'молдова': {u'latitude': u'474116310', u'longitude': u'283698850'}, u'псков': {u'latitude': u'578166994', u'longitude': u'283344734'}, u'австрия': {u'latitude': u'475162310', u'longitude': u'145500720'}, u'мальта': {u'latitude': u'359374959', u'longitude': u'143754160'}, u'якутск': {u'latitude': u'620354522', u'longitude': u'1296754745'}, u'северск': {u'latitude': u'566192692', u'longitude': u'848816834'}, u'киргизия': {u'latitude': u'412043800', u'longitude': u'747660980'}, u'индия': {u'latitude': u'205936840', u'longitude': u'789628800'}, u'чимкент': {u'latitude': u'423416846', u'longitude': u'695901009'}, u'кировская область': {u'latitude': u'584198528', u'longitude': u'502097248'}, u'углич': {u'latitude': u'575247896', u'longitude': u'383308361'}, u'австралия': {u'latitude': u'-252743979', u'longitude': u'1337751360'}, u'львов': {u'latitude': u'498396830', u'longitude': u'240297169'}, u'египет': {u'latitude': u'268205530', u'longitude': u'308024980'}, u'чита': {u'latitude': u'520515032', u'longitude': u'1134711906'}, u'серпухов': {u'latitude': u'549179562', u'longitude': u'374229963'}, u'белогорск': {u'latitude': u'509198950', u'longitude': u'1284833835'}, u'бельгия': {u'latitude': u'505038870', u'longitude': u'44699360'}, u'волжский': {u'latitude': u'488176494', u'longitude': u'447707294'}, u'тамбов': {u'latitude': u'527235979', u'longitude': u'414423062'}, u'бостон': {u'latitude': u'423600825', u'longitude': u'-710588801'}, u'сша': {u'latitude': u'370902400', u'longitude': u'-957128910'}, u'черновцы': {u'latitude': u'482920787', u'longitude': u'259358367'}, u'вологда': {u'latitude': u'592180665', u'longitude': u'398978052'}, u'рязань': {u'latitude': u'546095417', u'longitude': u'397125857'}, u'объединенные арабские эмираты': {u'latitude': u'234240760', u'longitude': u'538478180'}, u'туапсе': {u'latitude': u'441065180', u'longitude': u'390806454'}, u'нальчик': {u'latitude': u'434949918', u'longitude': u'436045132'}, u'кирово-чепецк': {u'latitude': u'585540671', u'longitude': u'499885606'}, u'хайфа': {u'latitude': u'327940463', u'longitude': u'349895710'}, u'казань': {u'latitude': u'558304307', u'longitude': u'490660806'}, u'новгород': {u'latitude': u'585255698', u'longitude': u'312741927'}, u'кисловодск': {u'latitude': u'439056013', u'longitude': u'427280948'}, u'германия': {u'latitude': u'511656909', u'longitude': u'104515260'}, u'япония': {u'latitude': u'362048239', u'longitude': u'1382529240'}, u'белая церковь': {u'latitude': u'497967977', u'longitude': u'301310853'}, u'гамбург': {u'latitude': u'535510845', u'longitude': u'99936818'}, u'долгопрудный': {u'latitude': u'559470640', u'longitude': u'374992754'}, u'минск': {u'latitude': u'539045397', u'longitude': u'275615244'}, u'мариуполь': {u'latitude': u'470971330', u'longitude': u'375433669'}, u'италия': {u'latitude': u'418719399', u'longitude': u'125673800'}, u'южно-сахалинск': {u'latitude': u'469641127', u'longitude': u'1427347556'}, u'биробиджан': {u'latitude': u'487803574', u'longitude': u'1329130744'}, u'сарапул': {u'latitude': u'564539288', u'longitude': u'537742184'}, u'иркутск': {u'latitude': u'522869740', u'longitude': u'1043050183'}, u'ростов-на-дону': {u'latitude': u'472357137', u'longitude': u'397015050'}, u'сочи': {u'latitude': u'436028078', u'longitude': u'397341543'}, u'кипр': {u'latitude': u'351264130', u'longitude': u'334298590'}, u'кызыл': {u'latitude': u'517150831', u'longitude': u'944574804'}, u'сербия': {u'latitude': u'440165210', u'longitude': u'210058589'}, u'чехов': {u'latitude': u'557702011', u'longitude': u'376024752'}, u'новосибирск': {u'latitude': u'550083525', u'longitude': u'829357327'}, u'сиэтл': {u'latitude': u'476062095', u'longitude': u'-1223320708'}, u'пущино': {u'latitude': u'548395772', u'longitude': u'376258923'}, u'ступино': {u'latitude': u'549040441', u'longitude': u'380803509'}, u'реутов': {u'latitude': u'557617579', u'longitude': u'378613023'}, u'саяногорск': {u'latitude': u'530966187', u'longitude': u'914164517'}, u'кокшетау': {u'latitude': u'532948229', u'longitude': u'694047872'}, u'республика карелия': {u'latitude': u'631558701', u'longitude': u'329905551'}, u'великобритания': {u'latitude': u'553780510', u'longitude': u'-34359729'}, u'тобольск': {u'latitude': u'582000240', u'longitude': u'682635227'}, u'грузия': {u'latitude': u'423154070', u'longitude': u'433568919'}, u'краснодар': {u'latitude': u'450392674', u'longitude': u'389872210'}, u'литва': {u'latitude': u'551694380', u'longitude': u'238812750'}, u'израиль': {u'latitude': u'310460510', u'longitude': u'348516119'}, u'братск': {u'latitude': u'561737660', u'longitude': u'1016038976'}, u'вашингтон': {u'latitude': u'389071923', u'longitude': u'-770368707'}, u'магнитогорск': {u'latitude': u'534129429', u'longitude': u'590016233'}, u'улан-удэ': {u'latitude': u'518238785', u'longitude': u'1076073380'}, u'винница': {u'latitude': u'492330830', u'longitude': u'284682170'}, u'атланта': {u'latitude': u'337489954', u'longitude': u'-843879824'}, u'сумы': {u'latitude': u'509077000', u'longitude': u'347981000'}, u'обнинск': {u'latitude': u'551170374', u'longitude': u'365970818'}, u'украина': {u'latitude': u'483794330', u'longitude': u'311655800'}, u'ухта': {u'latitude': u'635673210', u'longitude': u'537471594'}, u'тольятти': {u'latitude': u'535086002', u'longitude': u'494198344'}, u'мексика': {u'latitude': u'236345010', u'longitude': u'-1025527839'}, u'геленджик': {u'latitude': u'445918615', u'longitude': u'380241663'}, u'москва и область': {u'latitude': u'553403960', u'longitude': u'382917651'}, u'тула': {u'latitude': u'542048360', u'longitude': u'376184915'}, u'азербайджан': {u'latitude': u'401431050', u'longitude': u'475769270'}, u'миасс': {u'latitude': u'550506794', u'longitude': u'601034960'}, u'санкт-петербург и ленинградская область': {u'latitude': u'600793208', u'longitude': u'318926643'}, u'венгрия': {u'latitude': u'471624939', u'longitude': u'195033040'}, u'нижний новгород': {u'latitude': u'562965039', u'longitude': u'439360589'}, u'свердловская область': {u'latitude': u'590077350', u'longitude': u'619316226'}, u'красногорск': {u'latitude': u'558263313', u'longitude': u'373262970'}, u'ижевск': {u'latitude': u'568618600', u'longitude': u'532324285'}, u'симферополь': {u'latitude': u'449521170', u'longitude': u'341024169'}, u'железногорск': {u'latitude': u'562544955', u'longitude': u'935333646'}, u'выборг': {u'latitude': u'607139528', u'longitude': u'287571570'}, u'минеральные воды': {u'latitude': u'442116750', u'longitude': u'431238527'}, u'киров': {u'latitude': u'586035320', u'longitude': u'496667982'}, u'удмуртская республика': {u'latitude': u'570670218', u'longitude': u'530277947'}, u'жодино': {u'latitude': u'541016136', u'longitude': u'283471257'}, u'павловский посад': {u'latitude': u'557758031', u'longitude': u'386532915'}, u'клин': {u'latitude': u'563333815', u'longitude': u'367304470'}, u'греция': {u'latitude': u'390742080', u'longitude': u'218243120'}, u'кельн': {u'latitude': u'509375310', u'longitude': u'69602786'}, u'грозный': {u'latitude': u'433168796', u'longitude': u'456814855'}, u'энгельс': {u'latitude': u'514753296', u'longitude': u'461136773'}, u'черноголовка': {u'latitude': u'560096238', u'longitude': u'383853085'}, u'южная америка': {u'latitude': u'-87831950', u'longitude': u'-554914769'}, u'курск': {u'latitude': u'517091956', u'longitude': u'361562240'}, u'абакан': {u'latitude': u'537175644', u'longitude': u'914293172'}, u'ровно': {u'latitude': u'506199000', u'longitude': u'262516170'}, u'ямало-ненецкий ао': {u'latitude': u'660653057', u'longitude': u'769345194'}, u'польша': {u'latitude': u'519194380', u'longitude': u'191451360'}, u'выкса': {u'latitude': u'553262146', u'longitude': u'421701700'}, u'челябинская область': {u'latitude': u'544319421', u'longitude': u'608788962'}, u'пятигорск': {u'latitude': u'440498933', u'longitude': u'430396360'}, u'нижний тагил': {u'latitude': u'579214912', u'longitude': u'599816186'}, u'николаев': {u'latitude': u'469750329', u'longitude': u'319945830'}, u'казахстан': {u'latitude': u'480195730', u'longitude': u'669236840'}, u'черногория': {u'latitude': u'427086780', u'longitude': u'193743900'}, u'саранск': {u'latitude': u'542000477', u'longitude': u'451745115'}, u'ангарск': {u'latitude': u'525155702', u'longitude': u'1039171600'}, u'дзержинск': {u'latitude': u'562440992', u'longitude': u'434351804'}, u'пушкино': {u'latitude': u'559878329', u'longitude': u'378411773'}, u'китай': {u'latitude': u'358616600', u'longitude': u'1041953970'}, u'химки': {u'latitude': u'558940553', u'longitude': u'374439487'}, u'семей': {u'latitude': u'504233463', u'longitude': u'802508110'}, u'чернигов': {u'latitude': u'514982000', u'longitude': u'312893500'}, u'детройт': {u'latitude': u'423314270', u'longitude': u'-830457538'}, u'пенза': {u'latitude': u'532272903', u'longitude': u'450000000'}, u'калуга': {u'latitude': u'545518584', u'longitude': u'362850973'}, u'северная америка': {u'latitude': u'545259614', u'longitude': u'-1052551187'}, u'жуковский': {u'latitude': u'555974912', u'longitude': u'381132561'}, u'архангельск': {u'latitude': u'645472506', u'longitude': u'405601553'}, u'бразилия': {u'latitude': u'-142350040', u'longitude': u'-519252800'}, u'таганрог': {u'latitude': u'472416334', u'longitude': u'388676013'}, u'республика дагестан': {u'latitude': u'421431885', u'longitude': u'470949799'}, u'павлодар': {u'latitude': u'522873032', u'longitude': u'769674023'}, u'штутгарт': {u'latitude': u'487758459', u'longitude': u'91829321'}, u'глазов': {u'latitude': u'581368837', u'longitude': u'526548340'}, u'уссурийск': {u'latitude': u'438023133', u'longitude': u'1319630890'}, u'дубна': {u'latitude': u'567320202', u'longitude': u'371668973'}, u'мурманск': {u'latitude': u'689585244', u'longitude': u'330826598'}, u'словения': {u'latitude': u'461512410', u'longitude': u'149954629'}, u'россия': {u'latitude': u'615240100', u'longitude': u'1053187560'}, u'видное': {u'latitude': u'555470891', u'longitude': u'376986011'}, u'республика башкортостан': {u'latitude': u'542312171', u'longitude': u'561645257'}, u'мюнхен': {u'latitude': u'481351253', u'longitude': u'115819806'}, u'орехово-зуево': {u'latitude': u'558034354', u'longitude': u'389667902'}, u'щелково': {u'latitude': u'559170380', u'longitude': u'380369346'}, u'шахты': {u'latitude': u'477236223', u'longitude': u'402355138'}, u'липецк': {u'latitude': u'526121996', u'longitude': u'395981224'}, u'франкфурт-на-майне': {u'latitude': u'501109220', u'longitude': u'86821267'}, u'новочеркасск': {u'latitude': u'474177686', u'longitude': u'400726784'}, u'ачинск': {u'latitude': u'562360841', u'longitude': u'904903152'}, u'сызрань': {u'latitude': u'531504504', u'longitude': u'483978959'}, u'горно-алтайск': {u'latitude': u'519421860', u'longitude': u'859719355'}, u'сортавала': {u'latitude': u'617045423', u'longitude': u'306879016'}, u'набережные челны': {u'latitude': u'557185054', u'longitude': u'523721038'}, u'сыктывкар': {u'latitude': u'616478508', u'longitude': u'508339029'}, u'могилев': {u'latitude': u'539007158', u'longitude': u'303313597'}, u'омск': {u'latitude': u'549884804', u'longitude': u'733242362'}, u'майкоп': {u'latitude': u'445984115', u'longitude': u'401080868'}, u'астрахань': {u'latitude': u'463588045', u'longitude': u'480599345'}, u'невинномысск': {u'latitude': u'446380149', u'longitude': u'419504638'}, u'кривой рог': {u'latitude': u'479104830', u'longitude': u'333917830'}, u'татарстан': {u'latitude': u'551802364', u'longitude': u'507263945'}, u'арзамас': {u'latitude': u'553964609', u'longitude': u'438299175'}, u'армавир': {u'latitude': u'449873603', u'longitude': u'411111326'}, u'электросталь': {u'latitude': u'557835532', u'longitude': u'384551611'}, u'кемеровская область': {u'latitude': u'547574648', u'longitude': u'874055288'}, u'томск': {u'latitude': u'565010397', u'longitude': u'849924506'}, u'махачкала': {u'latitude': u'429666308', u'longitude': u'475126285'}, u'испания': {u'latitude': u'404636670', u'longitude': u'-37492199'}, u'дзержинский': {u'latitude': u'556260118', u'longitude': u'378491912'}, u'королёв': {u'latitude': u'559316797', u'longitude': u'378518551'}, u'зеленодольск': {u'latitude': u'558516037', u'longitude': u'485371528'}, u'чебоксары': {u'latitude': u'561167662', u'longitude': u'472627820'}, u'аргентина': {u'latitude': u'-384160970', u'longitude': u'-636166719'}, u'керчь': {u'latitude': u'453573139', u'longitude': u'364682929'}, u'луганск': {u'latitude': u'485740410', u'longitude': u'393078150'}, u'гейдельберг': {u'latitude': u'493987524', u'longitude': u'86724335'}, u'ужгород': {u'latitude': u'486207999', u'longitude': u'222878829'}, u'волгодонск': {u'latitude': u'475060474', u'longitude': u'421794335'}, u'владивосток': {u'latitude': u'431737387', u'longitude': u'1320064506'}, u'лос-анджелес': {u'latitude': u'340522342', u'longitude': u'-1182436848'}, u'бийск': {u'latitude': u'525072746', u'longitude': u'851472004'}, u'узбекистан': {u'latitude': u'413774910', u'longitude': u'645852620'}, u'элиста': {u'latitude': u'463154883', u'longitude': u'442794011'}, u'елабуга': {u'latitude': u'557631660', u'longitude': u'520254936'}, u'находка': {u'latitude': u'428222753', u'longitude': u'1328834039'}, u'салехард': {u'latitude': u'665500730', u'longitude': u'666028111'}, u'ивано-франковск': {u'latitude': u'489226330', u'longitude': u'247111169'}, u'суздаль': {u'latitude': u'564191590', u'longitude': u'404536152'}, u'кировоград': {u'latitude': u'485079330', u'longitude': u'322623169'}, u'салават': {u'latitude': u'533860436', u'longitude': u'559259471'}, u'ишим': {u'latitude': u'561146308', u'longitude': u'694771245'}, u'брянск': {u'latitude': u'532635305', u'longitude': u'344161099'}, u'орск': {u'latitude': u'512145242', u'longitude': u'585440566'}, u'владикавказ': {u'latitude': u'430252343', u'longitude': u'446659759'}}

    def __init__(self, zone, query, region=None, start=0, num=10, zone_params=None, always_params='as_dt=e', custom_params=None):
        self.zone = zone
        self.query = query
        self.region = region
        self.start = int(start) * num
        self.always_params = always_params
        self.num = int(num) if num else self.num
        self.custom_params = custom_params

        if zone_params:
            self.zone_params = zone_params

    def _get_crutch_zone(self):
        if self.zone == 'com.uag':
            return 'com.ua'
        return self.zone

    @classmethod
    def get_region_cookie(cls, region):
        from base64 import b64encode
        import time

        coords = cls.regions_coords.get(region.lower())
        if not coords:
            return {}

        coords = [coords['latitude'], coords['longitude']]
        n = 'role:1\n' \
            'producer:12\n' \
            'provenance:6\n' \
            'timestamp: {0}\n' \
            'latlng{{\n' \
            'latitude_e7:{1}\n' \
            'longitude_e7:{2}\n' \
            '}}\n' \
            'radius:65000'
        n = n.format(int(time.time()) * 100000, coords[0], coords[1])
        cookie_value = 'a+{0}'.format(b64encode(n))
        return {'UULE': cookie_value}

    def get_url(self):
        u"""Возвращает урл"""

        params = ''

        if self.num:
            params += '&num={0}'.format(self.num)

        if self.start:
            params += '&start={0}'.format(self.start)

        zone_params = self.zone_params.get(self.zone, {})
        hl = zone_params.get('hl')
        if hl:
            params += '&hl={0}'.format(hl)

        zone_custom = zone_params.get('custom', {})
        if zone_custom:
            params += '&{}'.format(zone_custom)

        if self.always_params:
            params += '&{}'.format(self.always_params)

        if self.region:
            params += '&near={0}'.format(urllib.quote(self.region))

        if self.custom_params:
            params += '&{0}'.format(self.custom_params)

        return self.base_url_tpl.format(
            zone=self._get_crutch_zone(), query=urllib.quote(self.query), params=params
        )
