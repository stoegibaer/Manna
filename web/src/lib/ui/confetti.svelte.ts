/** Global confetti trigger: every fire() starts a new burst ([big] for completed sections). */
class ConfettiState {
  trigger = $state(0)
  big = $state(false)
  fire(big = false) {
    this.big = big
    this.trigger++
  }
}
export const confetti = new ConfettiState()
