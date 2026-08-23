# 선택자를 사용하는 방법 (copy selector)
soup.select('태그명') # soup.select('h3')
soup.select('.클래스명') # soup.select('.some_class_name')
soup.select('#아이디명') # soup.select('#unique_id')
soup.select('상위태그명 > 하위태그명 > 하위태그명')
soup.select('상위태그명.클래스명 > 하위태그명.클래스명')

# 앞의 예에서처럼 여러 <li>를 가질 때 몇 번째 <li> 인지를
# 부모의 몇 번째 자식인지 명시해서 지정할 수도 있습니다. 
soup.select('.클래스명:nth-child(자식의순서)')

# 태그와 속성값으로 찾는 방법
soup.select('태그명[속성="값"]')

# 한 개만 가져오고 싶은 경우
soup.select_one('위와 동일')