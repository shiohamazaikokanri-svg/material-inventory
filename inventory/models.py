from django.db import models


class MaterialItem(models.Model):
    key = models.CharField(max_length=120, db_index=True)
    maker = models.CharField(max_length=120, blank=True)
    material = models.CharField(max_length=120, db_index=True)
    thickness = models.DecimalField(max_digits=10, decimal_places=3, db_index=True)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    length = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    weight = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    place = models.CharField(max_length=120, blank=True)
    address = models.CharField(max_length=255, blank=True)
    imported_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["material", "thickness", "width", "length", "key"]
        indexes = [
            models.Index(fields=["material", "thickness"]),
            models.Index(fields=["key", "material"]),
        ]

    def __str__(self):
        return f"{self.material} {self.thickness} x {self.width} x {self.length}"
