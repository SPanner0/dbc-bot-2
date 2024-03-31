use poise::serenity_prelude as serenity;

use crate::{
    database::{Database, PgDatabase},
    tournament_model::SingleElimTournament,
    BotError, Context,
};

use super::CommandsContainer;

pub struct OwnerCommands;

impl CommandsContainer<PgDatabase, SingleElimTournament> for OwnerCommands {
    fn get_commands_list(
    ) -> Vec<poise::Command<crate::BotData<PgDatabase, SingleElimTournament>, BotError>>
    {
        vec![]
    }
}

#[poise::command(slash_command, guild_only, owners_only)]
async fn set_manager(
    ctx: Context<'_>,
    #[description = "The Manager role"] role: serenity::Role,
) -> Result<(), BotError> {
    if ctx.guild().is_none() {
        ctx.send(
            poise::CreateReply::default()
                .content("This command can only be used in a server.")
                .ephemeral(true),
        )
        .await?;
    }

    let guild_id = ctx.guild().unwrap().id.to_string(); // This unwrap is safe
    let manager_role_id = role.id.to_string();

    ctx.data()
        .database
        .set_manager_role(guild_id, manager_role_id)
        .await?;

    Ok(())
}
