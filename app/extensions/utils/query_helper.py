class RawQueryHelper:
    """ model 대신 query만 전달되도록 해야 함"""

    @staticmethod
    def print_raw_query(query):
        # TODO : raw query 출력용 로그 작성
        print(str(query.statement.compile(compile_kwargs={"literal_binds": True})))
