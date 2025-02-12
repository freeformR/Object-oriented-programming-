import scipy.stats as stats  # Importing for norm.ppf (inverse normal CDF)

class SignalDetection:
    def __init__(self, hits, misses, fa, cr):
        """initializes the SignalDetection class with a count of:
        - Hits: number of correctly detected signals
        - Misses: number of undetected signals
        - False alarms: number of noise mistaken for a signal
        - Correct rejections: number of correctly identified noise
        """
        self.hits = hits
        self.misses = misses
        self.fa = fa
        self.cr = cr
#(ChatGPT assisted)
    def hit_rate(self):
        """Calculate the hit rate (H), which is the proportion 
        of correctly detecting a signal when it is present

        Formula:
        H = hits / (hits + misses)"""
        return self.hits / (self.hits + self.misses) if (self.hits + self.misses) > 0 else 0

    def fa_rate(self):
        """Calculate the false alarm rate (FA), which is the proportion 
        of incorrectly detecting a signal when none is present
        
        Formula:
        FA = fa / (fa + cr)"""
        return self.fa / (self.fa + self.cr) if (self.fa + self.cr) > 0 else 0

    def d_prime(self):
        """Calculate d-prime (d'), which is a measure of how well the 
        observer can distinguish signal and noise
        
        Higher d' indicates stronger/better sensitivity
        Lower d' indicates weaker sensitivity
        
        Formula:
        d' = Z(Hit Rate) - Z(False Alarm Rate)
        """
        H = self.hit_rate()
        FA = self.fa_rate()

#Avoid extreme probabilities (0 or 1) by applying a correction (ChatGPT assisted)
        H = min(max(H, 1e-5), 1 - 1e-5)
        FA = min(max(FA, 1e-5), 1 - 1e-5)

        return stats.norm.ppf(H) - stats.norm.ppf(FA)

    def criterion(self):
        """Calculate the criterion (C), which is a measure of the observer's response bias
        sees if they respond 'noise' or 'signal' more often

        Positive C suggests more likely to respond 'noise'
        Negative C suggests more likely to say 'signal'
        Near-zero C suggests no bias
        
        Formula:
        C = -0.5 * (Z(Hit Rate) + Z(False Alarm Rate))"""
        H = self.hit_rate()
        FA = self.fa_rate()

#Avoid extreme probabilities (0 or 1) by applying a correction
        H = min(max(H, 1e-5), 1 - 1e-5)
        FA = min(max(FA, 1e-5), 1 - 1e-5)

        return -0.5 * (stats.norm.ppf(H) + stats.norm.ppf(FA))

sd = SignalDetection(5, 2, 8, 2)
d_prime_value = sd.d_prime()
criterion_value = sd.criterion()
print(f"d': {d_prime_value}")
print(f"Criterion: {criterion_value}")