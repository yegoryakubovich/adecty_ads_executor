#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

def min2sec(minutes: int):
    return minutes * 60


def hour2sec(hours: int):
    return min2sec(hours * 60)


MAX_SESSION2ONE_PROXY = 3
DAY_OLD = 5
URL_FOR_TEST_PROXY = 'https://ifconfig.me/all.json'
BOT_SLEEP_MIN_SEC = min2sec(0)  # sleep min
BOT_SLEEP_MAX_SEC = min2sec(1)  # sleep max
ASSISTANT_SLEEP_SEC = min2sec(1)  # assistant sleep
SEND_MSG_DELAY_MSG = 3  # msg delay
SEND_MSG_DELAY_SEC = min2sec(10)  # msg delay

groups_list = ["@kekajangroup"]  # "adaptaciyausa", "adaptaciya_ua_usa"]
# "ads_new_york", "calosangeles", "ca_miami_chat", "chatamerika",
# "chatinnj", "chatinSeattle", "chatinsf", "chatnewyork1", "chchatua", "chicagoil", "la_services",
# "losangeles2021immigrants", "los_angeles_avito", "los_angeles_ca", "los_angeles_california_usa",
# "miamichatik", "miamichatru", "movingsf", "multinational_group", "nashaphiladelphia", "nashlosangeles",
# "nashmiami", "nashny", "newyorkchatru", "nyjobsusa", "philadelphiachat", "phillychat", "russianlo",
# "sacramentocity", "telemarketus", "ukrnewyorkgroup", "usachatru", "usaforuz", "usagreen", "usarmenians",
# "usa_360", "usb_mexico_usa", "uzbeksinusalup", "vatandoshimuzbus", "vatandoshim_usa_50_state",
# "vatandoshim_uz", "vatandoshimusa", "yagonadarchausany", "nomadsfamilyusa", "kg_america", "nashchicago",
# "nomadschicago", "sfnomad", "mahallanewyorkjobs", "nomadssd", "mexicousa21", "newyorknash1",
# "rentcarnomad", "rusoenmexico", "workersnomads", "ads_california", "america_new_york",
# "canada_work_life", "creditmebel908203131", "dogbanusa", "freeshipping", "horizont24", "housingnomad",
# "jobinmoving", "jobs_usa24", "jobsinny", "la_california", "liveintheusa", "mextous", "miamihotchat",
# "nomadsboston", "nomadsmiami", "nomadsdc", "nomadsfamily", "poputchiki_usa", "rent_miami_rusrek",
# "russianclassifieds", "teachbkusa", "trucker_cargo", "usa_benefit", "usa_exchange", "usa_job_help",
# "usa_job_helper", "usamexico", "used21cars", "biznesdvigusa", "miamiarea", "newyorkchat24",
# "newyork_job", "vhi7f", "mayami_360", "nomadsfamilyla", "nyjobs_usa", "in_miami"]

proxies_list = ["zrZ1na:vzSPV8@38.170.95.174:9504", "zrZ1na:vzSPV8@38.153.57.132:9851", "zrZna:vzSPV8@38.12.57.11:9851",
                "zrZ1na:vzSPV8@38.170.95.62:9805", "zrZ1na:vzSPV8@38.170.243.82:9329", "zrZ1na:vzSPV8@38.170.95.7:9460",
                "89wRmC:Hu2Dq6@94.131.19.93:9106", "89wRmC:Hu2Dq6@94.131.21.81:9190",
                "89wRmC:Hu2Dq6@94.131.19.197:9592", "89wRmC:Hu2Dq6@94.131.21.174:9726"]

strings = {
    "573213524152": {"phone": "573213524152", "user_id": 5619122397,
                     "string_session": "AQAAB_gAik9fS8Hf3Ubk7_FfHMKaXzGX2BnISq3OZHp2xwFBhAE33Lj9VGNvBB4uirpwZDEWRglrQF6pNDhfZNNUJLcdp5RAklOF6qdIhnBKgnwAAvjg1iSEtNdEC2ClxHZAIMstCgcEnrnxtieEn3fYGVss12quMdzIwmheUnWaNGiHpLc-4jXrVHmW9DCIUI8j4CyN8sqYEf8IS8EAT2grLPwSemT3tRwfD1wmGi8l5ZsmBpu8nikMaGYHILxJltuPJfinTFzRX231sk2gAFiR8KZIOob83eDFwT2T6Vn9cLtF_ReGyA5cCOP4tlNZxydaXr1D0DwdbVOsVqpMvFdP_VR-HwAAAAFO7QDdAA",
                     "api_id": 2040, "api_hash": "b18441a1ff607e10a989891a5462e627", "device_model": "PC 64bit",
                     "app_version": "3.2.2 x64", "system_version": "Windows 11"},
    "573213815626": {"phone": "573213815626", "user_id": 6067370896,
                     "string_session": "AQAAB_gAk9dBnBQzGHb7f6NHE0G0wdKPhhJMod1jhZ4khtryRuhNffhgtFZXhfLi2rurkbtgiP-d4m25UTGq1vi72TR9yw3u9xmKeOEudAaZYJonY5fhyzcpeMajgUxfjA3OnIDVM3cU-N78w6es5Eir9V2QcctA0Mj4OSkkSgf3k1vLcwTl_0-yvswlfGBI60aIsIRlLkQb6oVK06BtTjtast0NynS_3ZQmsAtmwUgYwJOgdLVMTSFGDW9q6mpRcjRBh4Tzocj0k2RqWoQ4ioKExbDQuI9YV1ZnaC9qkjAOLRJc28tbxpL1sOCT4eyKae1D_-d5cxsLAoKyKolzIy4B7rq3twAAAAFppLuQAA",
                     "api_id": 2040, "api_hash": "b18441a1ff607e10a989891a5462e627", "device_model": "PC 64bit",
                     "app_version": "3.2.3 x64", "system_version": "Windows 11"},
    "573214578014": {"phone": "573214578014", "user_id": 6235508623,
                     "string_session": "AQAAB_gAkz1jBBy8fSksA1mtZMlNN0hiG4-hf6xenhzKgQgjxhan494tXm-Cx-6zB1aPVsEeyg180vOYjTbSXvbilMbglGKrm8evFQ-8ZMFE7AEF1pPhG5lc9WJ84ssUMAEjmSKnTBIXj-J2nz6MRb75gpugKnxVqC8THeqnpIxhjjum7kCuCnDni-QamxNAckeA1Jl_UcTVRLRbupS797wkpKFPTnEPVR_omy5HJhRzsCD8pmitFWl_DXmvyilPViUNaCGuLqNTWerdcphkPKMDBdYpB99AtUSLZr0s0452wIrbyHXxzLMlx0Oye93wdzn7wN9g6oindcV0VWuS80G4UYTe1AAAAAFzqk-PAA",
                     "api_id": 2040, "api_hash": "b18441a1ff607e10a989891a5462e627", "device_model": "PC 64bit",
                     "app_version": "3.2.2 x64", "system_version": "Windows 10"},
    "19847881778": {"phone": "19847881778", "user_id": 6252154481,
                    "string_session": "AQAAB_gAVoCPWDjdmieC2uk-NpORX6pQSwskJ-QNqsGIMR-46Gi5KWnghClwynPKPKoDVmkFrDBvqh68Ap-pwA6WuLLsDk6OaP83GsMXKEvfkCgxM4H2RGtJ5KmvAY6_e7F1aihNTvYi43r5vvzCAO5VHwCH-MDPiZZp9IeWoVHVxkrdXAWP1giTi0tUm0s2K1d_Pd3cUTi1F7iyoSCiKgEtH14OR8nl6nik9puIrW-tWppaPYw6UmhMuH8urvW5FsbjBJ129p3SUXMcW46A5HXVIOWM1bqNQLyOqrG4zJMd5TEGqr2VDPkSQ_-ZQ4bJQ24JQuLR_7EOngy18BlAA71otuETVwAAAAF0qE5xAA",
                    "api_id": 2040, "api_hash": "b18441a1ff607e10a989891a5462e627", "device_model": "DESKTOP-VNZGM31",
                    "app_version": "3.1.3", "system_version": "Windows 8"},
    "19847881781": {"phone": "19847881781", "user_id": 5807235465,
                    "string_session": "AQAAB_gArQnWSd05nZxxoUaXSrcfk6rawYHTbsmY7JOQPoGebYcsWyJ6koWN0eJRnmt5neHyghRyUFholaoDTd3jWQYRlRfF3OQ2DGleDw2CgvxvqBVsztythu1wfS88meKc7clfE0s6H2UJdySov4qCe_9VMk9F7e9lxmbHG5k865We2CNOIv1XBxzV-8EZqZtB_8QglPpWJY7EjpGNizjGHEQB7wXXQ-dqjzsQMRMlnhtMLTuTZw1ek8SS-QAXAYjkCcSa2CbVHNrXxgEbwGneMJ1cdtobMP94O501ExqUrRtbi-CYNUs1D43ibS9QnNvmJ4ky9PuA_Bdnmene5QbD6nNrswAAAAFaI2GJAA",
                    "api_id": 2040, "api_hash": "b18441a1ff607e10a989891a5462e627", "device_model": "DESKTOP-0PHDO9G",
                    "app_version": "4.0.5", "system_version": "Windows 8.1"},
    "19847881814": {"phone": "19847881814", "user_id": 5965785956,
                    "string_session": "AQAAB_gApc2Zdyvb87-Wdaq6jQjbZnSQba6JGhk_ry_29FOolieK4_1_0Oc8yBCiA8_JWeEV9rLgcLOqLn0hN-vi79VzatW-NtNHIgGjmgm9rjUQ5lQ8S76A8B7QsP24N9UiNs39c8d_bDOkuB8e3MKhFNhDUVE-4f8MSTIng82G4w165V0-qGzn0Td23DKjYSJrV-NJFOpdKOzDD2xoqNUV3fK1RofSorA8xb3wC1M5uju84kX6OutUL7R3c9ukF8JY2XwJRK6Bh31AXddBdZaYw20-y_EoF2j1zIv8zaAGNPROAL2PFT1MsIVJNCAke-7yr6y17d4dEzz1Zu9f4bUCs_tZ0AAAAAFjlqtkAA",
                    "api_id": 2040, "api_hash": "b18441a1ff607e10a989891a5462e627", "device_model": "DESKTOP-5HE6MSQ",
                    "app_version": "4.2.2", "system_version": "Windows 8.1"},
    "19847881823": {"phone": "19847881823", "user_id": 5820150842,
                    "string_session": "AQAAB_gAruEzTp-a9w2Zkn5dqU20yMQbGCvhcvRgmsbg2CRzPKD1-fMc94jLoav4A60U6kTMIASSlKEb1y73gMD4yl_1FzkRetiuQQHGwiQaNsy9DJFMcdE0l796IegOQGPg2ISHV8enF6aP42kBmm9OEFqpW989ljBfIp4ZxRjpw1vCPjnjezMZMbHSfz5v4ZhQ8Voz8Do90nKBvhvkil1X69p1LCk-utitHLczem4zPJ6NnNTrGwcSuoAHDt5sMqFKKm34j4EN1fUsilF5gFSouFPgbmd1YlbgZUhCIHAZP30br0DujxNQwp7513qLSioVcN4ZKoBMUTd3amxLofJh2UErfAAAAAFa6HQ6AA",
                    "api_id": 2040, "api_hash": "b18441a1ff607e10a989891a5462e627", "device_model": "DESKTOP-TLL7EZT",
                    "app_version": "3.3.3", "system_version": "Windows 8.1"},
    "19847881902": {"phone": "19847881902", "user_id": 6231230207,
                    "string_session": "AQAAB_gAxPAiOYNSuBg68XO2YQr_x_8dRTr6eTP9fw4dwf_OUrBqNl9-aE0e4XCMSUgIIIjMsr9RYH9Xb_TSTJTcdFIk_0U8s5Pt8LYsJ4RtrjcDeSIC9Zi4k9NxMLk7JRviwH05C9ReNtByGdESGMs1Y-DpTBNn_bifeu40J9166XIiywdPA55Bjf_4lqLGXaWPBYLX42S-83tkpTWwR4A43kjFYbgkv4tuIcdSLt_Kr6TyHU6C_KYbidpEgrh-hBdZYwcaf5gRVZAbwKUYpdshznw9MIL_vuNhzaRgwSVtWw1Jd0eCmI0rRyeeC4kmJojQPT033hKSaLKLwMzleMZ-DwzJHgAAAAFzaQb_AA",
                    "api_id": 2040, "api_hash": "b18441a1ff607e10a989891a5462e627", "device_model": "DESKTOP-UPDAHTC",
                    "app_version": "4.0.0", "system_version": "Windows 8.1"},
    "19847881921": {"phone": "19847881921", "user_id": 6152506755,
                    "string_session": "AQAAB_gAKQA34rR6RMRwx0fc9WNQZ3uiUT_EclA78P1JaIr14ra2NqbeCDOrJb7RN7YTVnsV2qQ85dlmWlWkeymqPzkTXOz9sBCpr5_C1g6hk4DkUZWvlC-sRz_OH2T7phgID4R_U97wJWr5ec1f6cmDG5R7YWJUaLqTa8aYZJoTbFkI2vIXrU6yw7q1DbYZrZVFB0TPcnNljHXYVvYnYy_5YSCnJunDYunL91hK8rNOaA8kMs4cBfwVMikcAaUScr7iMR6FDL-mGFaCfJdHLxJEsCr7aoHTaHWNLZ9sWj_aBa7sM7BePvEC37jIPnPliggz4X7aFhvNWjWXY2rvKxO6SMFvxgAAAAFut82DAA",
                    "api_id": 2040, "api_hash": "b18441a1ff607e10a989891a5462e627", "device_model": "DESKTOP-ATRO9UK",
                    "app_version": "3.3.2", "system_version": "Windows 7"},
    "19847881945": {"phone": "19847881945", "user_id": 5923650901,
                    "string_session": "AQAAB_gAEt974SmoN2l78iq4I4bWI0HqUdSOhUq8_YOcyJtdLDI4RKDvcbF3Ar6htV9Ujtsdwc9PuTscrTtJkbwKA_9GPp13vb7Efnet3lgGDchz_EKKmfnNMJ4mfnI-k0UGPOuGJitf3eEza7MO7oTeJTjb3z5SPETVhOcBkN7FPRRQeHIM5xJgPHqJWKVrKBHoI1EOQBeqsagNKKAfXTZJEal3iuf5-TEalga9HWfDJeBa5huGLKBWp1gS2l8fREaOPRhCoshOllyLIxrC_wavNLuLGEOp-rxD7FGXNnaCbIU0sz6S4G9suitUzF1s4I1yHZCjYZeazpyawtGVXCuN5eBmFAAAAAFhE71VAA",
                    "api_id": 2040, "api_hash": "b18441a1ff607e10a989891a5462e627", "device_model": "DESKTOP-YKOKYKF",
                    "app_version": "4.1.4", "system_version": "Windows 7"},
    "19847881981": {"phone": "19847881981", "user_id": 6292548888,
                    "string_session": "AQAAB_gAhD9eFsB9-IR7bhucO5wbNHw7suMn7ixlkmi_AHQO9IzjefWZqqti7hgbFLopnZmUd5ClexBQXr-pnpk1n2HeXaQ96AAQA8whR5Se854e0DpsVk9yNsCTfCFl7ERfoE3ctT1oya5udD3zst6mFKFwzcbupIPlDZF-rDWZwdYXnGwhq9az-RG8Hfr653jXrPJoK7yIuSQ2WV_yJjKfA9kt6EmT8wC6klexrOZBD4hMizJtFMyLfWmHUl8N3eedUg1jYrezj7wlN553K8A0mcfvfkqH7-jFrgPSYGRd3jCv_N3KLYHl4qiXASo73AzTkhIftkKk7jntp_jYNtJTg8h_bwAAAAF3EK0YAA",
                    "api_id": 2040, "api_hash": "b18441a1ff607e10a989891a5462e627", "device_model": "DESKTOP-XVJ2JIG",
                    "app_version": "4.1.2", "system_version": "Windows 11"},
    "19847881983": {"phone": "19847881983", "user_id": 6045582752,
                    "string_session": "AQAAB_gAvwS0TVyLu0OkXqccugfm6YCB9WNC3Vd3kdX3LxtACcyR2ju0r6sp7iXw57597ctM5D1w2j281y3LHltzec8WPVXC8ZqKmNWMWbPQ2Te0mCqPNxWqoHfv7blGK51iInjxL0gJzB_IpAjWxI-iY9mdzBek_AG8mWy_1n5MhWgpkmmKSdRhOpk0n9dcxk3MQd_K3LSKEV6ofW0eXtsWFSvXY0M1mdeZGeQTg182JBGqHI88M6ztmrnCK-GMR1UBSF-XPXTuPO6Kf8TvwIGzoS7ZHV_zA2c2TVzKfu_gWcfJ2EQiqy4m0LPE3U1H43IQck4SS_PI1Nd6mRvrw_LPCokvQgAAAAFoWEWgAA",
                    "api_id": 2040, "api_hash": "b18441a1ff607e10a989891a5462e627", "device_model": "DESKTOP-ZN09NYD",
                    "app_version": "4.3.4", "system_version": "Windows 8.1"},
    "19854680099": {"phone": "19854680099", "user_id": 6025547018,
                    "string_session": "AQAAB_gAcAK9uJyfIzkI610lrI1MzccEs2XgkmWgJGRrG8zKYFhg6f38yzDF_d7gCTvG105dB9Ah_9V8nGkKn-bRsOjDcL4KEGIsTuc8BDNWsKVYClNsqt-WiOvRdBVYZyGpA_iF5r16HpBgqxsHe6Qf_FfHq0y8_-QGprKISNNq87SpJHBbbZ_ecAQGBDYUkVz_qJ-36I3t0b-bDumGB2ntZOyu-Xj2AyUtUoq9CbKS_wYe9d9hMW8LPl2Omw3fI-FzMibH1u1If37AzhTwOxr-DgXorrqVOPEunaMsIHvEHxeEWOMnvhIJKY6bxou8Eo2oqKEmekaS5xFA9FM1lRtqyYcAgwAAAAFnJo0KAA",
                    "api_id": 2040, "api_hash": "b18441a1ff607e10a989891a5462e627", "device_model": "DESKTOP-6XI7C0W",
                    "app_version": "4.2.3", "system_version": "Windows 11"},
    "573213524152": {"phone": "573213524152", "user_id": 5619122397,
                     "string_session": "AQAAB_gAik9fS8Hf3Ubk7_FfHMKaXzGX2BnISq3OZHp2xwFBhAE33Lj9VGNvBB4uirpwZDEWRglrQF6pNDhfZNNUJLcdp5RAklOF6qdIhnBKgnwAAvjg1iSEtNdEC2ClxHZAIMstCgcEnrnxtieEn3fYGVss12quMdzIwmheUnWaNGiHpLc-4jXrVHmW9DCIUI8j4CyN8sqYEf8IS8EAT2grLPwSemT3tRwfD1wmGi8l5ZsmBpu8nikMaGYHILxJltuPJfinTFzRX231sk2gAFiR8KZIOob83eDFwT2T6Vn9cLtF_ReGyA5cCOP4tlNZxydaXr1D0DwdbVOsVqpMvFdP_VR-HwAAAAFO7QDdAA",
                     "api_id": 2040, "api_hash": "b18441a1ff607e10a989891a5462e627", "device_model": "PC 64bit",
                     "app_version": "3.2.2 x64", "system_version": "Windows 11"},
    "573213815626": {"phone": "573213815626", "user_id": 6067370896,
                     "string_session": "AQAAB_gAk9dBnBQzGHb7f6NHE0G0wdKPhhJMod1jhZ4khtryRuhNffhgtFZXhfLi2rurkbtgiP-d4m25UTGq1vi72TR9yw3u9xmKeOEudAaZYJonY5fhyzcpeMajgUxfjA3OnIDVM3cU-N78w6es5Eir9V2QcctA0Mj4OSkkSgf3k1vLcwTl_0-yvswlfGBI60aIsIRlLkQb6oVK06BtTjtast0NynS_3ZQmsAtmwUgYwJOgdLVMTSFGDW9q6mpRcjRBh4Tzocj0k2RqWoQ4ioKExbDQuI9YV1ZnaC9qkjAOLRJc28tbxpL1sOCT4eyKae1D_-d5cxsLAoKyKolzIy4B7rq3twAAAAFppLuQAA",
                     "api_id": 2040, "api_hash": "b18441a1ff607e10a989891a5462e627", "device_model": "PC 64bit",
                     "app_version": "3.2.3 x64", "system_version": "Windows 11"},
    "573214578014": {"phone": "573214578014", "user_id": 6235508623,
                     "string_session": "AQAAB_gAkz1jBBy8fSksA1mtZMlNN0hiG4-hf6xenhzKgQgjxhan494tXm-Cx-6zB1aPVsEeyg180vOYjTbSXvbilMbglGKrm8evFQ-8ZMFE7AEF1pPhG5lc9WJ84ssUMAEjmSKnTBIXj-J2nz6MRb75gpugKnxVqC8THeqnpIxhjjum7kCuCnDni-QamxNAckeA1Jl_UcTVRLRbupS797wkpKFPTnEPVR_omy5HJhRzsCD8pmitFWl_DXmvyilPViUNaCGuLqNTWerdcphkPKMDBdYpB99AtUSLZr0s0452wIrbyHXxzLMlx0Oye93wdzn7wN9g6oindcV0VWuS80G4UYTe1AAAAAFzqk-PAA",
                     "api_id": 2040, "api_hash": "b18441a1ff607e10a989891a5462e627", "device_model": "PC 64bit",
                     "app_version": "3.2.2 x64", "system_version": "Windows 10"},
    "573215301480": {"phone": "573215301480", "user_id": 5668661854,
                     "string_session": "AQAAB_gAmTKcDZ-xa_-9qx120eHOV1VwoGqZ0Rr6pylDd_dkr7F_JfutABsjnmwdZaAb7f_btT7aGofQ6L_qIrG_sD5-iKAB-faH1ykcWtw4tDRvHna_wwYS3iI7Ek_JQzTCQIvnWCydeCrlFypBBfyXZo7OJv7v-Kocqdi_snF78SLXDGZEXLR-7J_QOKhlW_8LQwwLS4e_SbMyfnEjfkyfe564PXTLNnEWcHafka-ECsj25fX44pJIrlzKTX6gi3q65aZeWqdMe1ihTXNh2zwttlSfVCjfh0_f73fCx7gmLQhDNxgu_SIknIXSrFXzFW-r62d_h6p_OznLwuapWZDO0ODM3AAAAAFR4OpeAA",
                     "api_id": 2040, "api_hash": "b18441a1ff607e10a989891a5462e627", "device_model": "DESKTOP-XYSU66S",
                     "app_version": "3.1.5", "system_version": "Windows 7"},
    "573215421301": {"phone": "573215421301", "user_id": 6071152143,
                     "string_session": "AQAAB_gAAV7NC2iRiqSwLsKXvTiAoVgZemq2VFYYeCSJ2YHjbZ6lHA74fILz58TW9OdMg7w79rjLEP_KwmaXHbeKkA70Ob-EInlG2aaPVD4xqj6sQ_D8TItd3iXAKCEgTDbPR-z69GzC4xZvc1AVPXiwax52-ui6cVtSH1yXUyyIGNy2Slcqm5GfDuF9iFAGzY60t0AZ3PQ6cXyYwxNIid_1WFPkfAkcSzyyFq_w8KXOpNflwYVfjwwph24whifnTh1-Cat7s8zD4Vnu2BIenFaBjS2YFiqpZEvG8ucw8OpkxSacaVUGHjw1uyN5ASdwOuylq3Zz1gX9NgQa3z3kd2WQif2HhAAAAAFp3m4PAA",
                     "api_id": 2040, "api_hash": "b18441a1ff607e10a989891a5462e627", "device_model": "PC 64bit",
                     "app_version": "3.2.3 x64", "system_version": "Windows 11"}
}
