# print(get_age('bob'))  # 20
# print(get_age('carry'))  # 38

# fruits = ['사과','배','배','감','수박','귤','딸기','사과','배','수박']

# def count_fruits(something):
#     count = 0
#     for fruit in fruits:
#         if fruit == something:
#             count +=1
#     return count

# bae_count = count_fruits('배')
# print(bae_count)


people = [{'name': 'bob', 'age': 20}, 
          {'name': 'carry', 'age': 38},
          {'name': 'john', 'age': 7},
          {'name': 'smith', 'age': 17},
          {'name': 'ben', 'age': 27}]


def get_age(something):
    for person in people:
        if person['name'] == something:
            return person['age']
    return '해당하는 이름이 없습니다'


print(get_age('bob'))