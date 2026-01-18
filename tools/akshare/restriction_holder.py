import akshare as ak

# 解禁股东


if __name__ == '__main__':
    stock_restricted_release_stockholder_em_df = ak.stock_restricted_release_stockholder_em(symbol="600000",
                                                                                            date="20200904")
    print(stock_restricted_release_stockholder_em_df)
