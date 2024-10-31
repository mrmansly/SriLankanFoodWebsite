#!/bin/sh

set -e  # Exit immediately if a command exits with a non-zero status.

echo "Unsealing vault..."

# Array of unseal keys
UNSEAL_KEYS="$UNSEAL_KEY_1 $UNSEAL_KEY_2 $UNSEAL_KEY_3"

# Initialize counter
key_count=0

# Increment count for each defined key
[ -n "$UNSEAL_KEY_1" ] && key_count=$((key_count + 1))
[ -n "$UNSEAL_KEY_2" ] && key_count=$((key_count + 1))
[ -n "$UNSEAL_KEY_3" ] && key_count=$((key_count + 1))

# allow a bit of time for vault to be started successfully
sleep 5

if [ $key_count -lt 3 ]; then
  echo "Error: 3 UNSEAL_KEY environment variables have not been set."
  exit 1
fi

for KEY in $UNSEAL_KEYS; do
  if [ -z "$KEY" ]; then
    echo "Error: One or more unseal keys are not set."
    exit 1
  fi
done

# Unseal the Vault
for KEY in $UNSEAL_KEYS; do
  vault operator unseal "$KEY"
done

echo "Vault is unsealed."