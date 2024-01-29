from random import randint

# 서로 다른 2개의 소수 고르기
def is_prime(n):
    if n<2:
        return False        # 만약 n이 2보다 작다면 n은 소수가 아니기때문에 False를 반환
    for i in range(2, int(n **0.5)+1):     # 그렇지 않다면 i가 2와 n의 0.5제곱+1까지 반복된다.
        if n%i == 0:        # 만약 n나누기i의 나머지가 0이 될 때 까지 n을 돌리고
            return False    # 나머지가 0이 되면 소수가 아니기 때문에 false를 리턴한다.
    return True             # 반복문을 마치고 위의 모든 조건을 만족하지 않았다면 n은 소수 이므로 return True

def find_primes(start, end):        # 유클리드 호제법을 이용해 소수 찾기
    prime1 = prime2 = 0             # prime 변수 초기화, 선택된 소수 저장을 위해 사용
    while not is_prime(prime1):     # prime1이 소수가 아닌 동안 반복
        prime1 = randint(start, end -1)     # randit 함수를 사용하여 start부터 end-1사이의 임의의 정수를 prime1에 할당
    while not is_prime(prime2):     # prime2가 소수가 아닌 동안 반복
        prime2 = randint(start, end -1)     # randit 함수를 사용하여 start부터 end-1사이의 임의의 정수를 prime2에 할당
    return prime1, prime2   # 두 소수를 찾았다면 이를 튜플로 묶어서 반환, 임의의 소수를 받아와서 검증하고 할당

# ------------------------------------------------ #
# phi를 구하고 , 서로소인 e 구하기
# 유클리드 호제법 이용

def gcd(a,b):           # gcd 함수 정의 : 두 함수 a,b의 최대공약수를 구하는 유클리드 호제법 사용
    while b:            # b가 0이 될 때까지 반복
        a,b = b, a%b    # a를 b로, b를 a를 b로 나눈 나머지로 갱신
    return a        # 최종적으로 a가 최대공약수 , return a

def find_e(phi):        # 함수 finde_e 정의하기(phi)값을 받아서 공개키 지수 e 찾기
    e = None        
    for i in range(2,phi):  # 2부터 phi-1까지의 범위에서 반복
        if gcd(phi,i)==1:   # i와 phi의 최대공약수가 1인 경우 (서로소인 경우)
            e=i             # e에 i값 할당
            break
    return e                # 찾은 e를 반환 -- 공개키 지수 e를 찾는 과정 구현

def find_d(phi,e):          # Euler의 피 함수 값 phi와 공개키 지수 e를 받아 개인키 지수 d 찾음
    d = None                # d 초기화
    for i in range(phi//e, phi):    # phi//e 부터 phi-1까지의 범위에서 반복 , i 값 찾기
        if e*i%phi==1:
            d=i
            break           # RSA에서는 공개키 e와 개인키 d가 서로에 대한 역원관계여야 하므로 위 공식 성립해야함
    return d

# ------------------------------------------------ #
# 공개키

def generate_keys():
    n,e,d = 0, None, None       #변수 초기화 n은 공개키 모듈러스, e는 공개키 지수, d는 개인키 지수
    while e is None or d is None:   # e나 d가 값이 할당되지 않은 동안 반복
        prime1, prime2 = find_primes(10,100) # find_primes함수를 사용하여 1000과 10000 사이의 두 소수를 찾음, RSA에 사용되는 소수 찾기
        n = prime1 * prime2     # 두 소수 곱해서 n 계산 , 공개키의 모듈러스로 사용
        phi = (prime1 -1)*(prime2 -1)   # Euler의 피 함수값을 계산해 phi에 저장 / 개인키 생성에 활용
        e=find_e(phi)           # phi를 이용하여 공개키 지수 e를 find_d 함수로 찾기
        d=find_d(phi,e)         # 개인키 지수 d를 계산하기 위해 find_d 함수 사용 / 개인키의 지수 찾는 역할 
    return n,e,d                # n,e,d 공개키 및 개인키의 핵심 구성 요소로 사용 RSA키 쌍 생성 역할

# ------------------------------------------------ #
# 거듭 제곱 get_mod 구현

def get_mod(message, exp, n):
    result = message            # result 변주 message로 초기화
    for i in range(1,exp):      # exp 값까지 반복하는 루프
        result = (message**exp)%n   # message값을 exp번 거듭제곱, 그 결과 n으로 나눈 나머지 새로운 result 값으로 업데이트
    return result

# ------------------------------------------------ #
# 암호화 및 복호화

def encrypt(message, e, n):         # RSA에서 사용되는 공개키 암호화 수행, message에 암호화 할 메세지
    return get_mod(message, e, n)   # e 공개키 지수, 암호화에 사용 / n 공개키 모듈러스 , 암호화에 사용 / 메세지를 e번 거듭제곱, n으로 모듈러 연산

def decrypt(message, d, n):         # RSA에서 사용되는 개인키 복호화 수행, message에 복호화 할 메세지
    return get_mod(message, d, n)   # d 개인키 지수 , 복호화에 사용 / n 공개키 모듈러스, 복호화에 사용 / 메세지를 d번 거듭제곱, n으로 모듈러 연산

# ------------------------------------------------ #
# RSA 실행 메인 함수

def main():
    message: int = int(input('암호화할 숫자를 입력하세요:'))
    #message: int=6
    n, e, d = generate_keys()
    print(' 공개키 1 : ',n,'\n','공개키 2 : ', e,'\n','개인키 : ', d)
    encrypted = encrypt(message, e, n)
    print(' 암호화 된 숫자 : ', encrypted)
    decrypted = decrypt(encrypted, d, n)
    print(' 복호화 된 숫자 : ', decrypted)
    
if __name__=='__main__':
    main() 
