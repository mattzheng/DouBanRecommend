
import pandas as pd
import turicreate

def ItemRecommend(data,threshold = 0.9):
    m = turicreate.item_similarity_recommender.create(data,target="rating")
    nn = m.get_similar_items()
    item_data = nn.to_dataframe()
    return item_data[item_data.score>threshold]

if  __name__ == '__main__':
    book_excel_all = pd.read_csv('book_excel.csv')
    data = turicreate.SFrame({'user_id': book_excel_all.book_name,
                              'item_id': book_excel_all.type,
                              'rating': book_excel_all.scores})
    # usrid  : 书籍编号
    # itemid : 书籍主要类型
    # rating : 书籍排名
    item_data = ItemRecommend(data)
    item_data.to_csv('item_data_item.csv',index = False,encoding = 'utf-8')
