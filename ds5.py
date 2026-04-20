class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.arr = arr[:]                     # Store original array
        self.tree = [0] * (4 * self.n)        # Safe size
        self.construct(0, self.n - 1, 0)

    # Build tree
    def construct(self, start, end, index):
        if start == end:
            self.tree[index] = self.arr[start]
            return

        mid = (start + end) // 2
        self.construct(start, mid, 2 * index + 1)
        self.construct(mid + 1, end, 2 * index + 2)

        self.tree[index] = self.tree[2 * index + 1] + self.tree[2 * index + 2]

    # Query
    def query_range_sum(self, l, r):
        return self._query(0, self.n - 1, l, r, 0)

    def _query(self, start, end, l, r, index):
        # Complete overlap
        if l <= start and r >= end:
            return self.tree[index]

        # No overlap
        if r < start or l > end:
            return 0

        mid = (start + end) // 2
        return (self._query(start, mid, l, r, 2 * index + 1) +
                self._query(mid + 1, end, l, r, 2 * index + 2))

    # Update
    def update_value(self, i, new_value):
        diff = new_value - self.arr[i]
        self.arr[i] = new_value
        self._update(0, self.n - 1, i, diff, 0)

    def _update(self, start, end, i, diff, index):
        if i < start or i > end:
            return

        self.tree[index] += diff

        if start != end:
            mid = (start + end) // 2
            self._update(start, mid, i, diff, 2 * index + 1)
            self._update(mid + 1, end, i, diff, 2 * index + 2)


# ================= USER INPUT =================

# Input array
arr = list(map(int, input("Enter array elements: ").split()))
st = SegmentTree(arr)

print("\nSegment Tree:", st.tree)

# Query input
l, r = map(int, input("Enter query range (l r): ").split())

if l < 0 or r >= len(arr) or l > r:
    print("Invalid range!")
else:
    print("Sum in range [{}, {}] = {}".format(l, r, st.query_range_sum(l, r)))

# Update input
i, new_val = map(int, input("Enter index and new value: ").split())

if i < 0 or i >= len(arr):
    print("Invalid index!")
else:
    st.update_value(i, new_val)
    print("Updated Segment Tree:", st.tree)

    # Query again after update
    print("Updated sum in range [{}, {}] = {}".format(l, r, st.query_range_sum(l, r)))