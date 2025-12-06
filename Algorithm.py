def quicksort(nums):
  if len(nums) < 2:
      return nums
  pivot = nums[len(nums)//2]
  less, equal, greater = [], [], []
  for val in nums:
    if val < pivot:
      less.append(val)
    elif val > pivot:
      greater.append(val)
    else: # val == piv:
      equal.append(val)
  ret = quicksort(less)
  ret += equal
  ret += quicksort(greater)

  return ret
