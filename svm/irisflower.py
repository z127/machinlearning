from sklearn import svm
from pylab import mpl, plt
from sklearn.cross_validation import train_test_split
import numpy as np
def iris_type(s):
    it ={b'Iris-setosa':0, b'Iris-versicolor':1,b'Iris-virginica': 2}
    return it[s]

path ='H:/Mypapers/iris/iris.txt'

data=np.loadtxt(path, dtype=float ,delimiter=',',converters={4:iris_type})
#print(data)
#split(数据，分割位置，轴=1（水平分割） or 0（垂直分割）)。
x,y=np.split(data,(4,),axis=1)
#print(x)
x=x[:,:2]
#x = x[:, :2]是为方便后期画图更直观，故只取了前两列特征值向量训练
#print(x)
#取第二个二位数组
#print(x[:1])
#取第二个向量的第一个数
#print((x[:1])[0][0])
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, train_size=0.6)
# sklearn.model_selection.train_test_split随机划分训练集与测试集。
# train_test_split(train_data,train_target,test_size=数字, random_state=0)

#参数解释：

#train_data：所要划分的样本特征集

#train_target：所要划分的样本结果

#test_size：样本占比，如果是整数的话就是样本的数量

#random_state：是随机数的种子。

#print(x_test)
#kernel='linear'时，为线性核，C越大分类效果越好，但有可能会过拟合（defaul C=1）。

#kernel='rbf'时（default），为高斯核，gamma值越小，分类界面越连续；gamma值越大，分类界面越“散”，分类效果越好，但有可能会过拟合。

#decision_function_shape='ovr'时，为one v rest，即一个类别与其他类别进行划分，

#decision_function_shape='ovo'时，为one v one，即将类别两两之间进行划分，用二分类的方法模拟多分类的结果。
clf = svm.SVC(C=0.8, kernel='rbf', gamma=20, decision_function_shape='ovr')
clf.fit(x_train,y_train.ravel())
#而numpy.ravel()返回的是视图（view，也颇有几分C/C++引用reference的意味），会影响（reflects）原始矩阵
#print(clf.score(x_train, y_train))
y_hat = clf.predict(x_train)
#print(y_hat)
y_hat2 = clf.predict(x_test)
#print (y_hat2)

#print ('decision_function:\n', clf.decision_function(x_train))
#decision_function中每一列的值代表距离各类别的距离。
#print ('\npredict:\n', clf.predict(x_train))

#绘制图形
x1_min, x1_max = x[:, 0].min(), x[:, 0].max()  # 第0列的范围
x2_min, x2_max = x[:, 1].min(), x[:, 1].max()  # 第1列的范围
x1, x2 = np.mgrid[x1_min:x1_max:200j, x2_min:x2_max:200j]  # 生成网格采样点
#print ("x1",x1)
#x1.flat转化为1维矩阵即列矩阵
#np.stackaxis为1，代表以列的形式扩展
grid_test = np.stack((x1.flat, x2.flat), axis=1)  # 测试点
print("grid_test\n",grid_test[180:230])
#transpose是转置矩阵
#print("x1=\n",x1.transpose()[0])
#flat转置为1维数组
#print("x1=\n",x1.flat)
grid_hat = clf.predict(grid_test)
print('grid_hat = \n', grid_hat)
# 预测分类值
grid_hat = grid_hat.reshape(x1.shape)
# 使之与输入的形状相同

mpl.rcParams['font.sans-serif'] = [u'SimHei']
mpl.rcParams['axes.unicode_minus'] = False
#绘制
#pcolormesh(x,y,z,cmap)这里参数代入x1，x2，grid_hat，cmap=cm_light绘制的是背景。

#scatter中edgecolors是指描绘点的边缘色彩，s指描绘点的大小，cmap指点的颜色。

#xlim指图的边界。
#
cm_light = mpl.colors.ListedColormap(['#A0FFA0', '#FFA0A0', '#A0A0FF']) #绿,红,紫
cm_dark = mpl.colors.ListedColormap(['g', 'r', 'b'])
plt.pcolormesh(x1, x2, grid_hat , cmap=cm_light)
print(grid_hat)
plt.scatter(x[:, 0], x[:, 1], c=y, edgecolors='k', s=50, cmap=cm_dark)  # 样本
plt.scatter(x_test[:, 0], x_test[:, 1], s=120, facecolors='none', zorder=10)  # 圈中测试集样本
plt.xlabel(u'花萼长度', fontsize=13)
plt.ylabel(u'花萼宽度', fontsize=13)
plt.xlim(x1_min, x1_max)
plt.ylim(x2_min, x2_max)
plt.title(u'鸢尾花SVM二特征分类', fontsize=15)
# plt.grid()
plt.show()