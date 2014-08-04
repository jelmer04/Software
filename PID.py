import time

class PID:
    kp = 0
    ki = 0
    kd = 0
    lasttime = 0
    setpoint = 50
    lastinput = 0
    sampletime = 1
    integral = 0
    outputmax = 1
    outputmin = 0
    output = 0
    auto = True

    def compute(self, inputvalue):
        if not self.auto:
            return

        # How long since calculation
        now = time.clock()
        deltatime = now - self.lasttime

        if deltatime >= self.sampletime:
            # Calculate error values
            error = self.setpoint - inputvalue
            self.integral += error * self.ki
            self.integral = self.clamp(self.integral)
            diff = inputvalue - self.lastinput

            # Compute PID output
            output = self.kp * error + self.integral - self.kd * diff
            self.output = self.clamp(output)

            # Remember some values for next time
            self.lasttime = now
            self.lastinput = inputvalue

        return self.output

    def tune(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki * self.sampletime
        self.kd = kd / self.sampletime
        return

    def set_sample_time(self, sampletime):
        if sampletime > 0:
            ratio = sampletime / self.sampletime
            self.ki *= ratio
            self.kd /= ratio
            self.sampletime = sampletime
        return

    def clamp(self, value):
        if value > self.outputmax:
            value = self.outputmax
        elif value < self.outputmin:
            value = self.outputmin
        return value

    def set_limits(self, outputmax, outputmin):
        if outputmin > outputmax:
            return

        self.outputmin = outputmin
        self.outputmax = outputmax

        self.integral = self.clamp(self.integral)
        return

    def run(self, auto):
        if auto and not self.auto:
            self.integral = self.clamp(self.output)
        self.auto = auto
        return