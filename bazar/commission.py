from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import AgentCommission, SaleCommission, SaleReferralCommission, SaleRankCommission, SaleCompanyCommission, Earning

@login_required
def agent_commission_list(request):
    agent_commissions = AgentCommission.objects.filter(agent=request.user.agent_profile)
    return render(request, 'commission/agent_commission_list.html', {'agent_commissions': agent_commissions})


@login_required
def admin_agent_commission_list(request):
    agent_commissions = AgentCommission.objects.all()
    return render(request, 'commission/admin_agent_commission_list.html', {'agent_commissions': agent_commissions})


@login_required
def sale_commission_list(request):
    sale_commissions = SaleCommission.objects.filter(user=request.user)
    return render(request, 'commission/sale_commission_list.html', {'sale_commissions': sale_commissions})


@login_required
def admin_sale_commission_list(request):
    sale_commissions = SaleCommission.objects.all()
    return render(request, 'commission/admin_sale_commission_list.html', {'sale_commissions': sale_commissions})


@login_required
def sale_referral_commission_list(request):
    sale_referral_commissions = SaleReferralCommission.objects.filter(referrer=request.user)
    return render(request, 'commission/sale_referral_commission_list.html', {'sale_referral_commissions': sale_referral_commissions})


@login_required
def admin_sale_referral_commission_list(request):
    sale_referral_commissions = SaleReferralCommission.objects.all()
    return render(request, 'commission/admin_sale_referral_commission_list.html', {'sale_referral_commissions': sale_referral_commissions})


@login_required
def sale_rank_commission_list(request):
    sale_rank_commissions = SaleRankCommission.objects.filter(registered_user=request.user)
    return render(request, 'commission/sale_rank_commission_list.html', {'sale_rank_commissions': sale_rank_commissions})

@login_required
def admin_sale_rank_commission_list(request):
    sale_rank_commissions = SaleRankCommission.objects.all()
    return render(request, 'commission/admin_sale_rank_commission_list.html', {'sale_rank_commissions': sale_rank_commissions})


@login_required
def sale_company_commission_list(request):
    sale_company_commissions = SaleCompanyCommission.objects.all()
    return render(request, 'commission/sale_company_commission_list.html', {'sale_company_commissions': sale_company_commissions})


@login_required
def earning_detail(request):
    earnings = Earning.objects.filter(user=request.user)
    return render(request, 'commission/earning_detail.html', {'earnings': earnings})


@login_required
def admin_earning_detail(request):
    earnings = Earning.objects.all()
    return render(request, 'commission/admin_earning_detail.html', {'earnings': earnings})