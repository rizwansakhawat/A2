from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from .models import Bank, Branch
from .forms import BankForm, BranchForm
from django.contrib.auth.models import User


# /banks/add/
@method_decorator(login_required, name='dispatch')
class AddBankView(View):
    def get(self, request):
        form = BankForm()
        return render(request, 'banks/add_bank.html', {'form': form})

    def post(self, request):
        form = BankForm(request.POST)
        if form.is_valid():
            bank = form.save(commit=False)
            bank.owner = request.user
            bank.save()
            return redirect(f'/banks/{bank.id}/details/')
        return render(request, 'banks/add_bank.html', {'form': form})
        

# /banks/<bank_id>/branches/add/
@method_decorator(login_required, name='dispatch')
class AddBranchView(View):
    def get(self, request, bank_id):
        bank = Bank.objects.filter(id=bank_id).first()
        if not bank:
            return HttpResponse(status=404)
        if bank.owner != request.user:
            return HttpResponse(status=403)
        form = BranchForm(initial={'email': 'admin@enigmatix.io'})
        return render(request, 'banks/add_branch.html', {'form': form})

    def post(self, request, bank_id):
        bank = Bank.objects.filter(id=bank_id).first()
        if not bank:
            return HttpResponse(status=404)
        if bank.owner != request.user:
            return HttpResponse(status=403)
        form = BranchForm(request.POST)
        if form.is_valid():
            branch = form.save(commit=False)
            branch.bank = bank
            branch.save()
            return redirect(f'/banks/branch/{branch.id}/details/')
        return render(request, 'banks/add_branch.html', {'form': form})
        

# /banks/all/
class AllBanksView(View):
    def get(self, request):
        banks = Bank.objects.all()
        return render(request, 'banks/all_banks.html', {'banks': banks})


# /banks/<bank_id>/details/
class BankDetailsView(View):
    def get(self, request, bank_id):
        bank = Bank.objects.filter(id=bank_id).first()
        if not bank:
            return HttpResponse(status=404)
        branches = bank.branches.all()
        return render(request, 'banks/bank_details.html', {'bank': bank, 'branches': branches})


#  /banks/branch/<branch_id>/details/
class BranchDetailsView(View):
    def get(self, request, branch_id):
        branch = Branch.objects.filter(id=branch_id).first()
        if not branch:
            return HttpResponse(status=404)
        data = {
            'id': branch.id,
            'name': branch.name,
            'transit_num': branch.transit_num,
            'address': branch.address,
            'email': branch.email,
            'capacity': branch.capacity,
            'last_modified': branch.last_modified.isoformat(),
        }
        return JsonResponse(data)


#  /banks/branch/<branch_id>/edit/
@method_decorator(login_required, name='dispatch')
class EditBranchView(View):
    def get(self, request, branch_id):
        branch = Branch.objects.filter(id=branch_id).first()
        if not branch:
            return HttpResponse(status=404)
        if branch.bank.owner != request.user:
            return HttpResponse(status=403)
        form = BranchForm(instance=branch)
        return render(request, 'banks/edit_branch.html', {'form': form})

    def post(self, request, branch_id):
        branch = Branch.objects.filter(id=branch_id).first()
        if not branch:
            return HttpResponse(status=404)
        if branch.bank.owner != request.user:
            return HttpResponse(status=403)
        form = BranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            return redirect(f'/banks/branch/{branch.id}/details/')
        return render(request, 'banks/edit_branch.html', {'form': form})
