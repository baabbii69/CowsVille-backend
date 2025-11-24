"""
Management command to create sample data for testing.
This creates farms, cows, and related data for development and testing.
"""

import random
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from FarmManager.models import (BreedType, Cow, Doctor, Farm, FeedingFrequency,
                                FloorType, GeneralHealthStatus,
                                GynecologicalStatus, HousingType, Inseminator,
                                MastitisStatus, Reproduction,
                                UdderHealthStatus, WaterSource)


class Command(BaseCommand):
    help = "Create sample data (farms, cows, inseminators, doctors) for testing"

    def add_arguments(self, parser):
        parser.add_argument(
            "--farms",
            type=int,
            default=5,
            help="Number of farms to create (default: 5)",
        )
        parser.add_argument(
            "--cows-per-farm",
            type=int,
            default=10,
            help="Number of cows per farm (default: 10)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        num_farms = options["farms"]
        cows_per_farm = options["cows_per_farm"]
        clear_existing = options["clear"]

        if clear_existing:
            self.stdout.write(self.style.WARNING("Clearing existing data..."))
            Cow.objects.all().delete()
            Farm.objects.all().delete()
            Inseminator.objects.all().delete()
            Doctor.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Existing data cleared"))

        # Ensure choice models are populated
        self.stdout.write("Ensuring choice models are populated...")
        from django.core.management import call_command

        call_command("populate_choices")

        # Get choice model instances
        housing_types = list(HousingType.objects.all())
        floor_types = list(FloorType.objects.all())
        water_sources = list(WaterSource.objects.all())
        feeding_frequencies = list(FeedingFrequency.objects.all())
        breed_types = list(BreedType.objects.all())
        gynecological_statuses = list(GynecologicalStatus.objects.all())

        if not all(
            [
                housing_types,
                floor_types,
                water_sources,
                feeding_frequencies,
                breed_types,
                gynecological_statuses,
            ]
        ):
            self.stdout.write(
                self.style.ERROR(
                    "Choice models are not populated. Run populate_choices first."
                )
            )
            return

        # Create Inseminators
        self.stdout.write("Creating inseminators...")
        inseminators = []
        for i in range(3):
            inseminator, created = Inseminator.objects.get_or_create(
                name=f"Inseminator {i+1}",
                defaults={
                    "phone_number": f"+25191100000{i+1}",
                    "address": f"Address {i+1}, Addis Ababa",
                    "is_active": True,
                },
            )
            inseminators.append(inseminator)
        self.stdout.write(
            self.style.SUCCESS(f"Created {len(inseminators)} inseminators")
        )

        # Create Doctors
        self.stdout.write("Creating doctors...")
        doctors = []
        for i in range(2):
            doctor, created = Doctor.objects.get_or_create(
                license_number=f"LIC{i+1:03d}",
                defaults={
                    "name": f"Doctor {i+1}",
                    "phone_number": f"+25191100001{i+1}",
                    "address": f"Clinic {i+1}, Addis Ababa",
                    "specialization": random.choice(
                        [
                            "Veterinary Medicine",
                            "Livestock Health",
                            "Reproductive Health",
                        ]
                    ),
                    "is_active": True,
                },
            )
            doctors.append(doctor)
        self.stdout.write(self.style.SUCCESS(f"Created {len(doctors)} doctors"))

        # Create Farms
        self.stdout.write(f"Creating {num_farms} farms...")
        farms = []
        for i in range(num_farms):
            farm = Farm.objects.create(
                farm_id=f"FARM{str(i+1).zfill(3)}",
                owner_name=f"Owner {i+1}",
                address=f"Farm Address {i+1}, Addis Ababa, Ethiopia",
                telephone_number=f"+25191234567{i}",
                location_gps=f"9.0{i},38.7{i}",
                cluster_number=f"CLUSTER{(i % 3) + 1}",
                fertility_camp_no=(i % 5) + 1,
                total_number_of_cows=cows_per_farm,
                number_of_calves=random.randint(1, min(5, cows_per_farm // 2)),
                number_of_milking_cows=random.randint(
                    max(1, cows_per_farm - 3), max(1, cows_per_farm - 1)
                ),
                total_daily_milk=random.randint(50, 200),
                type_of_housing=random.choice(housing_types),
                type_of_floor=random.choice(floor_types),
                main_feed="Hay, Silage, Concentrate",
                rate_of_cow_feeding=random.choice(feeding_frequencies),
                source_of_water=random.choice(water_sources),
                rate_of_water_giving=random.choice(feeding_frequencies),
                farm_hygiene_score=random.randint(1, 4),
                inseminator=random.choice(inseminators) if inseminators else None,
                doctor=random.choice(doctors) if doctors else None,
            )
            farms.append(farm)
        self.stdout.write(self.style.SUCCESS(f"Created {len(farms)} farms"))

        # Create Cows
        self.stdout.write(f"Creating {cows_per_farm} cows per farm...")
        total_cows = 0
        for farm in farms:
            for j in range(cows_per_farm):
                # Calculate age (between 1 and 10 years)
                age_years = random.randint(1, 10)
                date_of_birth = date.today() - timedelta(
                    days=age_years * 365 + random.randint(0, 365)
                )

                # Determine sex (mostly female for dairy farms)
                sex = "F" if random.random() > 0.1 else "M"

                cow = Cow.objects.create(
                    farm=farm,
                    cow_id=f"{farm.farm_id}-COW{str(j+1).zfill(3)}",
                    breed=random.choice(breed_types),
                    date_of_birth=date_of_birth,
                    sex=sex,
                    parity=random.randint(0, 5) if sex == "F" else 0,
                    body_weight=random.uniform(300, 700),
                    bcs=random.choice([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]),
                    gynecological_status=random.choice(gynecological_statuses),
                    lactation_number=random.randint(0, 5) if sex == "F" else 0,
                    days_in_milk=random.randint(0, 300) if sex == "F" else 0,
                    average_daily_milk=random.uniform(5, 25) if sex == "F" else 0,
                )
                total_cows += 1

                # Create some reproduction records for female cows
                if sex == "F" and random.random() > 0.3:
                    Reproduction.objects.create(
                        farm=farm,
                        cow=cow,
                        heat_signs_seen=str(random.choice([True, False])),
                        heat_sign_start=timezone.now()
                        - timedelta(days=random.randint(1, 30)),
                        heat_sign_recorded_at=timezone.now()
                        - timedelta(days=random.randint(1, 30)),
                        is_cow_pregnant=random.choice([True, False]),
                        pregnancy_date=(
                            date.today() - timedelta(days=random.randint(1, 100))
                            if random.random() > 0.5
                            else None
                        ),
                    )

        self.stdout.write(self.style.SUCCESS(f"Created {total_cows} cows"))

        # Summary
        self.stdout.write(self.style.SUCCESS("\n" + "=" * 50))
        self.stdout.write(self.style.SUCCESS("Sample data created successfully!"))
        self.stdout.write(self.style.SUCCESS("=" * 50))
        self.stdout.write(f"Farms: {Farm.objects.count()}")
        self.stdout.write(f"Cows: {Cow.objects.count()}")
        self.stdout.write(f"Inseminators: {Inseminator.objects.count()}")
        self.stdout.write(f"Doctors: {Doctor.objects.count()}")
        self.stdout.write(f"Reproductions: {Reproduction.objects.count()}")
        self.stdout.write(self.style.SUCCESS("=" * 50))
