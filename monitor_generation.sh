#!/bin/bash
# Monitor all 6 generation processes

echo "Monitoring 6 parallel generation processes..."
echo "=================================="

pids=(
  "b5b88fd6-5402-4fb6-9cd0-6d9290b22582"  # Grade 4 Nonfiction
  "b023bd2c-b693-4812-a047-5bfc0795f7e7"  # Grade 5 Nonfiction
  "2465fd5e-1869-4e04-a082-acb3e22b8d8e"  # Grade 6 Nonfiction
  "88bc3aed-af05-4830-9a8d-695d7598029a"  # Grade 4 Narrative
  "898195fb-d7c9-4c01-81b2-c6650e15dcb1"  # Grade 5 Narrative
  "6ee4cfa7-7756-4023-be62-b1eac8d88c47"  # Grade 6 Narrative
)

# Wait for all to complete
wait

echo "All assessments generated!"
