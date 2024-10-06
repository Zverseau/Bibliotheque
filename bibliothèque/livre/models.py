from django.db import models
from django.core.exceptions import ValidationError


class Livre(models.Model):
    titre = models.CharField(max_length=30)  # Réduit à 50 caractères
    auteur = models.CharField(max_length=30)  # Réduit à 50 caractères
    nbr_en_stock = models.IntegerField()
    description = models.TextField(max_length=500)  # Limiter à 500 caractères
    isbn = models.CharField(max_length=13, unique=True, db_index=True)  # ISBN reste inchangé
    photo = models.ImageField(upload_to='media/')

    def rechercher_livre(self):
        pass

    def historique_livre(self):
        pass

    def __str__(self):
        return self.titre


class Bibliothecaire(models.Model):
    nom = models.CharField(max_length=30)  # Réduit à 30 caractères
    prenom = models.CharField(max_length=30)  # Réduit à 30 caractères
    email = models.EmailField(max_length=70, unique=False, db_index=True)  # Garde la longueur
    telephone = models.CharField(max_length=15, db_index=True)
    photo = models.ImageField(upload_to='media/')

    livres = models.ManyToManyField(Livre, related_name='gerer', blank=True)

    def authentifier(self):
        pass

    def ajouter_livre(self, titre, auteur, nbr_en_stock, description, isbn, photo):
        # Validation de l'ISBN pour s'assurer qu'il est unique
        if Livre.objects.filter(isbn=isbn).exists():
            raise ValidationError("Un livre avec cet ISBN existe déjà.")
        
        # Création du livre
        livre = Livre(
            titre=titre,
            auteur=auteur,
            nbr_en_stock=nbr_en_stock,
            description=description,
            isbn=isbn,
            photo=photo
        )
        livre.save()
        #return livre

    def afficher_tous_les_livres(self):
        livres = Livre.objects.all()
        return livres

    def modifier_info_livre(self, livre_id, titre=None, auteur=None, nbr_en_stock=None, description=None, isbn=None, photo=None):
        try:
            livre = Livre.objects.get(id=livre_id)
            
            if titre is not None:
                livre.titre = titre
            if auteur is not None:
                livre.auteur = auteur
            if nbr_en_stock is not None:
                livre.nbr_en_stock = nbr_en_stock
            if description is not None:
                livre.description = description          
            if photo is not None:
                livre.photo = photo
            if isbn is not None:
                if Livre.objects.filter(isbn=isbn).exclude(id=id).exists():
                    raise ValidationError("Un autre livre avec cet ISBN existe déjà.")
                livre.isbn = isbn

            livre.save()
            return livre
        except Livre.DoesNotExist:
            raise ValidationError("Le livre avec l'ID spécifié n'existe pas.")
        
        
    def supprimer_livre(self, livre_id):
        try:
            livre = Livre.objects.get(id=livre_id)
            livre.delete()
            return f"Livre '{livre.titre}' supprimé avec succès."
        except Livre.DoesNotExist:
            raise ValidationError("Le livre avec l'ID spécifié n'existe pas.")


class Emprunter(models.Model):
    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('retournee', 'Retourné'),
        ('en_retard', 'En retard'),
    ]

    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    email = models.EmailField(max_length=70, unique=False, db_index=True)
    telephone = models.CharField(max_length=15, db_index=True)
    photo = models.ImageField(upload_to='media/')
    date_retour = models.DateField()
    date_emprunt = models.DateField()
    statut_emprunt = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_cours')


    def __str__(self):
        return f'Emprunt: {self.livre} par {self.nom} {self.prenom}'
    
class authUser(models.Model):
    nom= models.CharField(max_length=30)
    prenom= models.CharField(max_length=30)
    mot_de_passe= models.CharField(max_length=30)
