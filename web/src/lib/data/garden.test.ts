import { test } from 'node:test'
import assert from 'node:assert/strict'
import { AFTER_LIFE, LIFE, ORDER, choicePending, offers, progress } from './garden.ts'
import { nextIndex, type Plan } from './plan.ts'

test('first tree needs 30, then each 40', () => {
  assert.equal(progress(29).done, 0)
  assert.equal(progress(30).done, 1)
  assert.equal(progress(30).inTree, 0)
  assert.equal(progress(69).done, 1)
  assert.equal(progress(70).done, 2)
  assert.equal(progress(470).done, 12)
  assert.equal(progress(510).done, 13)
  assert.equal(AFTER_LIFE, 510)
})

test('fruits ripen every four sections after the tree of life', () => {
  assert.equal(progress(509).fruits, 0)
  assert.equal(progress(513).fruits, 0)
  assert.equal(progress(514).fruits, 1)
  assert.equal(progress(510 + 144).fruits, 36)
  assert.equal(progress(2000).t, 1)
})

test('growth is visible with every section', () => {
  let last = -1
  for (let s = 0; s < 30; s++) {
    const t = progress(s).t
    assert.ok(t > last, `section ${s}`)
    last = t
  }
})

test('choice is pending until the next tree is planted', () => {
  const senf = ['senf']
  assert.equal(choicePending(29, senf), false)
  assert.equal(choicePending(30, senf), true)
  assert.equal(choicePending(30, [...senf, 'oel']), false)
  assert.equal(choicePending(150, [...senf, 'oel']), true)
  assert.equal(choicePending(470, ORDER), true)
  assert.equal(choicePending(470, [...ORDER, LIFE]), false)
  assert.equal(choicePending(5000, [...ORDER, LIFE]), false)
})

test('offers shrink towards the end and end with the tree of life', () => {
  assert.deepEqual(offers(['senf']), ['oel', 'feige', 'mandel'])
  assert.deepEqual(offers(ORDER.slice(0, -1)), ['akazie'])
  assert.equal(offers(ORDER.slice(0, -2)).length, 2)
  assert.deepEqual(offers(ORDER), [LIFE])
  assert.deepEqual(offers([...ORDER, LIFE]), [])
})

test('offers rotate so a tree not taken comes back', () => {
  const second = offers(['senf', 'oel'])
  assert.deepEqual(second, ['mandel', 'palme', 'zeder'])
  assert.ok(!second.includes('feige'))
})

const plan: Plan = { id: 'p', title: 'P', sections: ['a', 'b', 'c'].map((id) => ({ id, refs: [], title: id, summary: '' })) }

test('first run skips done sections', () => {
  assert.equal(nextIndex(plan, new Set(), undefined), 0)
  assert.equal(nextIndex(plan, new Set(['a', 'c']), undefined), 1)
  assert.equal(nextIndex(plan, new Set(['a', 'b', 'c']), undefined), -1)
})

test('reread follows its position even if everything is done', () => {
  const all = new Set(['a', 'b', 'c'])
  assert.equal(nextIndex(plan, all, 0), 0)
  assert.equal(nextIndex(plan, all, 2), 2)
  assert.equal(nextIndex(plan, all, 3), -1)
})
