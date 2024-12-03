from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Credit, Client, Paiement, PlanningPaiements, Garantie, HistoriquePaiement
from .form import ClientForm, ClientUpForm, CreditForm, CreditUpForm, PlanningForm, PlanningUpForm, PaiementForm, PaiementUpForm, GarantieForm, GarantieUpForm
from django.db.models import Q
from django.core.paginator import Paginator

# TemplateView
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_credits'] = Credit.objects.count()
        context['total_clients'] = Client.objects.count()
        context['total_garanties'] = Garantie.objects.count()
        context['credits_en_cours'] = Credit.objects.filter(statut='en cours').count()
        context['credits_paye'] = Credit.objects.filter(statut='payé')
        context['credits_en_retard'] = Credit.objects.filter(statut='retard')
        return context

# ListView
class ClientList(ListView):
    template_name = 'Clients/clients.html'
    model = Client
    context_object_name = "lesclients"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recherche = self.request.GET.get("query", "")
        if recherche:
            clients = Client.objects.filter(
                Q(id__icontains=recherche) | 
                Q(nom__icontains=recherche) | 
                Q(prenom__icontains=recherche)
                )
        else:
            clients = Client.objects.all()
        paginator = Paginator(clients, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['lesclients'] = page_obj
        context['query'] = recherche
        return context

    def get_queryset(self):
        recherche = self.request.GET.get("query", "")
        if recherche:
            return Client.objects.filter(
                Q(id__icontains=recherche) |
                Q(nom__icontains=recherche) |
                Q(prenom__icontains=recherche))
        else:
            return Client.objects.all()

class CreditList(ListView):
    model = Credit
    template_name = 'Credits/credits.html'
    context_object_name = 'lescredits'
    paginate_by = 5

    def get_queryset(self):
        queryset = Credit.objects.all()
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date:
            queryset = queryset.filter(date_debut__gte=start_date)
        if end_date:
            queryset = queryset.filter(date_fin__lte=end_date)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        page_number = self.request.GET.get('page')
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_obj = paginator.get_page(page_number)
        context['lescredits'] = page_obj
        return context

class PlanningPaiementList(ListView):
    model = PlanningPaiements
    template_name = 'Planning_Paiements/planning_paiements.html'
    context_object_name = "lesplannings"
    paginate_by = 5

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            recherche = self.request.GET.get("query", "")
            if recherche:
                Plannings = PlanningPaiements.objects.filter(
                    Q(id__icontains=recherche) | 
                    Q(credit__client__nom__icontains=recherche) | 
                    Q(credit__client__prenom__icontains=recherche) |
                    Q(date_echeance__icontains=recherche) |
                    Q(statut__icontains=recherche)
                    )
            else:
                Plannings = PlanningPaiements.objects.all()
            paginator = Paginator(Plannings, self.paginate_by)
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context['lesplannings'] = page_obj
            context['query'] = recherche
            return context

    def get_queryset(self):
        recherche = self.request.GET.get("query", "")
        if recherche:
            return PlanningPaiements.objects.filter(
                Q(id__icontains=recherche) |
                Q(credit__client__nom__icontains=recherche) |
                Q(credit__client__prenom__icontains=recherche) |
                Q(date_echeance__icontains=recherche)  |
                Q(statut__icontains=recherche)
                ) 
        else:
            return PlanningPaiements.objects.all()

class PaiementList(ListView):
    template_name = 'Paiements/paiements.html'
    model = Paiement
    context_object_name = "lespaiements"
    paginate_by = 5

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            recherche = self.request.GET.get("query", "")
            if recherche:
                Paiements = Paiement.objects.filter(
                    Q(id__icontains=recherche) |
                    Q(date_paiement__icontains=recherche) |
                    Q(mode_paiement__icontains=recherche)
                )
            else:
                Paiements = Paiement.objects.all()
            paginator = Paginator(Paiements, self.paginate_by)
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context['lespaiements'] = page_obj
            context['query'] = recherche
            return context

    def get_queryset(self):
        recherche = self.request.GET.get("query", "")
        if recherche:
            return Paiement.objects.filter(
                Q(id__icontains=recherche) |
                Q(date_paiement__icontains=recherche) |
                Q(mode_paiement__icontains=recherche)
            ) 
        else:
            return Paiement.objects.all()
    
class GarantieList(ListView):
    template_name = 'Garanties/garanties.html'
    model = Garantie
    context_object_name = "lesgaranties"
    paginate_by = 5

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            recherche = self.request.GET.get("query", "")
            if recherche:
                garanties = Garantie.objects.filter(
                    Q(id__icontains=recherche) |
                    Q(type_garantie__icontains=recherche) |
                    Q(valeur_estimee__icontains=recherche) |
                    Q(description__icontains=recherche) |
                    Q(statut__icontains=recherche) |
                    Q(credit__id__icontains=recherche)
                )
            else:
                garanties = Garantie.objects.all()
            paginator = Paginator(garanties, self.paginate_by)
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context['lesgaranties'] = page_obj
            context['query'] = recherche
            return context

    def get_queryset(self):
        recherche = self.request.GET.get("query", "")
        if recherche:
            return Garantie.objects.filter(
                Q(id__icontains=recherche) |
                Q(type_garantie__icontains=recherche) |
                Q(valeur_estimee__icontains=recherche) |
                Q(description__icontains=recherche) |
                Q(statut__icontains=recherche) |
                Q(credit__id__icontains=recherche)
            ) 
        else:
            return Garantie.objects.all()

class HistoriquePaiementList(ListView):
    template_name = 'Historique_Paiements/historiques.html'
    model = HistoriquePaiement
    context_object_name = "leshistoriques"
    paginate_by = 5

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            recherche = self.request.GET.get("query", "")
            if recherche:
                historiques = HistoriquePaiement.objects.filter(
                    Q(id__icontains=recherche) |
                    Q(remarque__icontains=recherche)
                )
            else:
                historiques = HistoriquePaiement.objects.all()
            paginator = Paginator(historiques, self.paginate_by)
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context['leshistoriques'] = page_obj
            context['query'] = recherche
            return context

    def get_queryset(self):
        recherche = self.request.GET.get("query", "")
        if recherche:
            return HistoriquePaiement.objects.filter(
                Q(id__icontains=recherche) |
                Q(remarque__icontains=recherche)
            ) 
        else:
            return HistoriquePaiement.objects.all()

# DetailView
class ClientDetail(DetailView):
    template_name = 'Clients/clientDetail.html'
    model = Client
    context_object_name = "leclient"
    pk_url_kwarg = "id"

class CreditDetail(DetailView):
    template_name = 'Credits/creditDetail.html'
    model = Credit
    context_object_name = "lecredit"
    pk_url_kwarg = "id"

class PlanningDetail(DetailView):
    template_name = 'Planning_Paiements/planningDetail.html'
    model = PlanningPaiements
    context_object_name = "leplanning"
    pk_url_kwarg = "id"

class PaiementDetail(DetailView):
    template_name = 'Paiements/paiementDetail.html'
    model = Paiement
    context_object_name = "lepaiement"
    pk_url_kwarg = "id"

class GarantieDetail(DetailView):
    template_name = 'Garanties/garantieDetail.html'
    model = Garantie
    context_object_name = "lagarantie"
    pk_url_kwarg = "id"

class HistoriqueDetail(DetailView):
    template_name = 'Historique_Paiements/historiqueDetail.html'
    model = HistoriquePaiement
    context_object_name = "lhistorique"
    pk_url_kwarg = "id"

# CreateView
class ClientCreate(CreateView):
    template_name = 'Clients/clientCreate.html'
    model = Client
    form_class = ClientForm
    success_url = '/credit/clients/'

class CreditCreate(CreateView):
    template_name = 'Credits/creditCreate.html'
    model = Credit
    form_class = CreditForm
    success_url = '/credit/credits/'

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form, 'errors': form.errors})

class PlanningCreate(CreateView):
    template_name = 'Planning_Paiements/planningCreate.html'
    model = PlanningPaiements
    form_class = PlanningForm
    success_url = '/credit/planning-paiements/'

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form, 'errors': form.errors})

class PaiementCreate(CreateView):
    template_name = 'Paiements/paiementCreate.html'
    model = Paiement
    form_class = PaiementForm
    success_url = '/credit/paiements/'

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form, 'errors': form.errors})

class GarantieCreate(CreateView):
    template_name = 'Garanties/garantieCreate.html'
    model = Garantie
    form_class = GarantieForm
    success_url = '/credit/garanties'

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form, 'errors': form.errors})

# UpdateView
class ClientUpdate(UpdateView):
    template_name = 'Clients/clientUpdate.html'
    model = Client
    form_class = ClientUpForm
    pk_url_kwarg = "id"
    success_url = '/credit/clients/'

class CreditUpdate(UpdateView):
    template_name  = 'Credits/creditUpdate.html'
    model = Credit
    form_class = CreditUpForm
    pk_url_kwarg = "id"
    success_url = '/credit/credits'

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form, 'errors': form.errors})
    
class PlanningUpdate(UpdateView):
    template_name = 'Planning_Paiements/planningUpdate.html'
    model = PlanningPaiements
    form_class = PlanningUpForm
    pk_url_kwarg = "id"
    success_url = '/credit/planning-paiements/'

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form, 'errors': form.errors})
    
class PaiementUpdate(UpdateView):
    template_name = 'Paiements/paiementUpdate.html'
    model = Paiement
    form_class = PaiementUpForm
    pk_url_kwarg = "id"
    success_url = '/credit/paiements/'

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form, 'errors': form.errors})
    
class GarantieUpdate(UpdateView):
    template_name = 'Garanties/garantieUpdate.html'
    model = Garantie
    form_class = GarantieUpForm
    pk_url_kwarg = 'id'
    success_url = '/credit/garanties'

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form, 'errors': form.errors})

# DeleteView
class ClientDelete(DeleteView):
    template_name = 'Clients/clients.html'
    model = Client
    pk_url_kwarg = "id"
    success_url = '/credit/clients/'

class CreditDelete(DeleteView):
    template_name = 'Credits/credits.html'
    model = Credit
    pk_url_kwarg = "id"
    success_url = '/credit/credits'

class PlanningDelete(DeleteView):
    template_name = 'Planning_Paiements/planning_paiements.html'
    model = PlanningPaiements
    pk_url_kwarg = "id"
    success_url = '/credit/planning-paiements/'

class PaiementDelete(DeleteView):
    template_name = 'Paiements/paiements.html'
    model = Paiement
    pk_url_kwarg = "id"
    success_url = '/credit/paiements'

class GarantieDelete(DeleteView):
    template_name = 'Garanties/garanties.html'
    model = Garantie
    pk_url_kwarg = "id"
    success_url = '/credit/garanties'

class HistoriqueDelete(DeleteView):
    template_name = 'Historiques/historiques.html'
    model = HistoriquePaiement
    pk_url_kwarg = "id"
    success_url = '/credit/historiques'