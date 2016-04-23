# -*- coding: UTF-8 -*-
listt = [[1,2,3],[3,4,2],[3,4]]
print list(set(listt[0]).intersection(*listt[1:]))