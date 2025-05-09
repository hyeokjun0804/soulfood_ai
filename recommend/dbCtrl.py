import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


# PostgreSQL 연결 정보를 반환하는 함수
def connect_field():
    fields = {
        "host": "localhost",  # PostgreSQL 서버의 호스트 주소
        "username": "postgres",  # PostgreSQL 사용자 이름
        "password": "1111",  # PostgreSQL 비밀번호
        "database": "soulfood",  # 연결할 데이터베이스 이름
        "port": 5432  # PostgreSQL 포트 번호
    }
    return fields


# PostgreSQL 데이터베이스에서 지정된 테이블의 데이터를 가져오는 함수
def bring_dataframe_from_table(table):
    # PostgreSQL 연결 문자열을 생성
    fields = connect_field()
    conn = f"postgresql+psycopg2://{fields['username']}:{fields['password']}@{fields['host']}:{fields['port']}/{fields['database']}"

    try:
        # 데이터베이스 엔진을 생성
        engine = create_engine(conn)
        query = f"SELECT * FROM {table}"  # 지정된 테이블의 모든 데이터를 가져오는 쿼리
        df = pd.read_sql(query, con=engine)  # SQL 쿼리를 실행하여 데이터 프레임에 저장
    except SQLAlchemyError as e:
        # 예외가 발생한 경우 에러 메시지를 출력
        print(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")
        return
    else:
        # 데이터베이스 연결을 닫고 완료 메시지를 출력
        engine.dispose()
        print("데이터가 성공적으로 선택되고 연결이 종료되었습니다!")
    return df


# DataFrame 데이터를 PostgreSQL 테이블에 삽입하는 함수
def insert_data_into_table(df, table):
    # PostgreSQL 연결 정보를 가져옴
    fields = connect_field()
    # PostgreSQL 연결 문자열 생성
    conn = f"postgresql+psycopg2://{fields['username']}:{fields['password']}@{fields['host']}:{fields['port']}/{fields['database']}"

    try:
        # with 문을 사용하여 자동으로 연결을 종료하도록 설정
        with create_engine(conn).connect() as connection:
            # DataFrame 데이터를 PostgreSQL 테이블에 삽입 (이미 테이블이 있으면 데이터를 추가)
            df.to_sql(table, con=connection, if_exists='append', chunksize=1000, index=False)
            print(f"테이블 '{table}'에 데이터가 성공적으로 삽입되었습니다.")
    except SQLAlchemyError as e:
        # 에러가 발생하면 에러 메시지를 출력
        print(f"데이터를 삽입하는 중 오류가 발생했습니다: {e}")
    else:
        print("데이터가 성공적으로 삽입되고 연결이 종료되었습니다!")
