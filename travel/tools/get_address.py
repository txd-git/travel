
#获取传输过来的地址
# def get_addree(position):
#     print(position)
#     address={}
#     for i in range(len(position)):
#         if position[i] == '省':
#             for s in range(i, len(position)):
#                 if position[s] == '市':
#                     shi = position[i + 1:s]
#                     address['shi']=shi
#                     for q in range(s, len(position)):
#                         if position[q] == '区' or position[q] == '县':
#                             qu = position[s + 1:q]
#                             address['qu'] = qu
#                             for v in range(q, len(position)):
#                                 if position[v] == '镇':
#                                     zhen = position[q + 1:v]
#                                     address['zhen'] = zhen
#
#
#
#     if not address:
#         address['shi']=position
#         address['qu']=position
#         address['zhen']=position
#     return address


def get_addree(position):
    print(position)
    address = {}
    if '省' in position:
        for i in range(len(position)):
            if position[i] == '省':
                for s in range(i, len(position)):
                    if position[s] == '市':
                        shi = position[i + 1:s]
                        address['shi']=shi
                        for q in range(s, len(position)):
                            if position[q] == '区' or position[q] == '县':
                                qu = position[s + 1:q]
                                address['qu'] = qu
                                for v in range(q, len(position)):
                                    if position[v] == '镇':
                                        zhen = position[q + 1:v]
                                        address['zhen'] = zhen
    elif '市' in position:
        for s in range(len(position)):
            if position[s] == '市':
                shi = position[:s]
                address['shi']=shi
                for q in range(s, len(position)):
                    if position[q] == '区' or position[q] == '县':
                        qu = position[s + 1:q]
                        address['qu'] = qu

                        for v in range(q, len(position)):
                            if position[v] == '镇':
                                zhen = position[q + 1:v]
                                address['zhen'] = zhen
                            else:
                                address['zhen'] = ''
                    elif position[q] == '镇':
                        address['qu'] = ''
                        zhen = position[s + 1:q]
                        address['zhen'] = zhen
                    else:
                        address['qu'] = ''
                        address['zhen'] = ''

    elif '区' in position:
        for q in range(len(position)):
            if position[q] == '区':
                qu = position[:q]
                address['shi'] = ''
                address['qu'] = qu
                for v in range(q, len(position)):
                    if position[v] == '镇':
                        zhen = position[q + 1:v]
                        address['zhen'] = zhen
                    else:
                        address['zhen'] = ''
    elif '县' in position:
        for q in range(len(position)):
            if position[q] == '县':
                qu = position[:q]
                address['shi'] = ''
                address['qu'] = qu
                for v in range(q, len(position)):
                    if position[v] == '镇':
                        zhen = position[q + 1:v]
                        address['zhen'] = zhen
                    else:
                        address['zhen'] = ''
    elif '镇' in position:
        for v in range(len(position)):
            if position[v] == '镇':
                zhen = position[:v]
                address['shi'] = ''
                address['qu'] = ''
                address['zhen'] = zhen

    if not address:
        address['shi'] = position
        address['qu'] = position
        address['zhen'] = position
    print('addresslide',address)
    return address

# get_addree('句容市石马镇船山村东侧')


