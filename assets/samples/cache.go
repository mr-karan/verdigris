// Package cache is a small TTL cache with a bounded size.
package cache

import (
	"context"
	"errors"
	"sync"
	"time"
)

// ErrNotFound is returned when a key is missing or has expired.
var ErrNotFound = errors.New("cache: key not found")

const defaultTTL = 5 * time.Minute

// Cache maps keys to values that expire after a fixed TTL.
type Cache[K comparable, V any] struct {
	mu    sync.RWMutex
	items map[K]entry[V]
	ttl   time.Duration
}

// Get returns the live value for key, or ErrNotFound.
func (c *Cache[K, V]) Get(ctx context.Context, key K) (V, error) {
	c.mu.RLock()
	defer c.mu.RUnlock()

	e, ok := c.items[key]
	if !ok || time.Now().After(e.expires) {
		var zero V
		return zero, fmt.Errorf("get %v: %w", key, ErrNotFound)
	}
	return e.value, nil
}
