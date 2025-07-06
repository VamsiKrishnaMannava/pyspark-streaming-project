'''
Given an integer array “nums” sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once. The relative order of the elements should be kept the same. Then return the number of unique elements in “nums”
Change the array “nums” such that the first “k” elements of “nums” contain the unique elements in the order they were present in “nums” initially. The remaining elements of “nums” are not important as well as the size of “nums”
 
Example:
 
Input: nums = [0,0,1,1,1,2,2,3,3,4]
Output: 5, nums = [0,1,2,3,4,`_,_,_,_,_`]
Explanation: Your function should return k = 5, with the first five elements of nums being 0, 1, 2, 3, and 4 respectively.
It does not matter what you leave beyond the returned k (hence they are underscores).
'''
from typing import List
class YouAnswer:

   def removeDuplicates(self, nums: List[int]) -> int:
      x = []
      s = set()
      for i in nums:
         if i in s:
            x.append('_')
         else:
            x.append(i)
            s.add(i)

      print(sorted(x,key=lambda x: x == '_'))
      print(len(s))
      return None
   
nums = [0,0,1,1,1,2,2,3,3,4]

print(f"nums={nums}")
k = YouAnswer().removeDuplicates(nums)
print(k)

