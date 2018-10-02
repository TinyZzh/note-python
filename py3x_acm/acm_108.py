


def twoSum(nums, target):
    for i in range(len(nums)):
        a = target-nums[i]
    if a in nums and i != nums.index(a):
        return([i, nums.index(a)])


if __name__ == "__main__":
    print(twoSum([1, 2, 3, 4], 5))
