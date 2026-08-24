# LRUCache - ELI5

## What this is

A small store that remembers up to a fixed number of things. When it is full and gets one more, it forgets the thing nobody has asked for in the longest time.

## The basic facts

- Memory is limited, so a store cannot keep everything (true everywhere, not just here).
- The store may hold at most a fixed number of items, chosen when it is created, and that number must be at least one.
- Things asked for recently tend to be asked for again soon (the file assumes this but does not say it).

## How it works

1. When the store is created, it is given its size limit, and refuses a limit of zero or less.
2. When someone asks for an item by name, the store looks for it.
3. If the item is not there, the store answers with nothing.
4. If it is there, the store hands it back and moves it to the "most recent" end of the line.
5. When someone stores an item, it goes to the "most recent" end of the line, replacing any old item with the same name.
6. If the store now holds more than its limit, it throws away the item at the other end. That is the one untouched for the longest time.

## Why it is this way

The file says the store drops the least recently used item when full. It does not say why recent use is the right thing to measure. It does not say why a size of zero is refused.

## Words you will see

- LRU: least recently used, the item nobody has touched for the longest time.
- capacity: the size limit.
- OrderedDict: a list of named items that remembers the order they were added or last moved in.
